#!/usr/bin/python3

import os
import sys
import signal
import json
import asyncio

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape

from dtos import *
from enums import *
from config import *
from messages import *
from models import *
from routes import Routes, Templates
from storage import *

from typing import Optional, Dict

from notifications import EmailNotifier
from handlers.auth import *

PRODUCTION_LINE_HAS_FAILURE : bool = False

_client_sockets: set = set()
_ui_sockets: set = set()

def broadcast_to_ui(message: dict):
    broadcast_message(_ui_sockets, message)

def notify_new_order(order):
    broadcast_to_ui(build_message(Messages.new_order, order.to_dict()))

def notify_order_started(order):
    broadcast_to_ui(build_message(Messages.order_started, order.to_dict()))

def notify_order_completed(order):
    broadcast_to_ui(build_message(Messages.order_completed, order.to_dict()))

def notify_order_progress(order):
    broadcast_to_ui(build_message(Messages.order_progress, order.to_dict()))

def notify_order_failed():
    broadcast_to_ui(build_message(Messages.order_failed, {}))

def notify_clear_failure():
    broadcast_to_ui(build_message(Messages.clear_failure, {}))

class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            Templates.index,
            Routes=Routes,
            Messages=Messages,
            ws_endpoint=UI_ENDPOINT
        )
    
    @tornado.web.authenticated
    def post(self):
        global PRODUCTION_LINE_HAS_FAILURE

        name = self.get_argument("name")

        qa   = int(self.get_argument("quantity_a"))
        qb   = int(self.get_argument("quantity_b"))
        qc   = int(self.get_argument("quantity_c"))

        order = add_order(name, qa, qb, qc)
        print(f"New order created: {order}", flush=True)

        notify_new_order(order)

        if not PRODUCTION_LINE_HAS_FAILURE:
            retry_message = build_message(Messages.order_retry, extra_object={})
            broadcast_message(_client_sockets, retry_message)

        self.redirect(Routes.home)

class UIWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global PRODUCTION_LINE_HAS_FAILURE

        print("UI client connected", flush=True)
        _ui_sockets.add(self)

        pending   = [o.to_dict() for o in get_orders_by_status(OrderStatus.PENDING)]
        in_prog   = [o.to_dict() for o in get_orders_by_status(OrderStatus.IN_PROGRESS)]
        completed = [o.to_dict() for o in get_orders_by_status(OrderStatus.COMPLETED)]

        init_msg = {
            "type": Messages.init_ui,
            "extra": {
                "pending": pending,
                "in_progress": in_prog,
                "completed": completed,
                "has_failure": PRODUCTION_LINE_HAS_FAILURE
            }
        }

        self.write_message(json.dumps(init_msg))

    def on_close(self):
        print("UI client disconnected", flush=True)
        _ui_sockets.discard(self)

    def on_message(self, raw):
        global PRODUCTION_LINE_HAS_FAILURE

        response_type, extra = extract_type_and_extra(raw)

        if not PRODUCTION_LINE_HAS_FAILURE:
            return
        
        if(response_type == Messages.clear_failure):
            PRODUCTION_LINE_HAS_FAILURE = False

            clear_failure_message = build_message(Messages.clear_failure, {})
            broadcast_message(_client_sockets, clear_failure_message)

            notify_clear_failure()

class ClientWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Client has connected...", flush=True)
        _client_sockets.add(self)

    def on_close(self):
        print("Client has disconnected...", flush=True)
        _client_sockets.discard(self)

    def on_message(self, raw):
        response_type, extra = extract_type_and_extra(raw)

        if(response_type == Messages.order_request):
            self._handle_order_request(extra)
        elif(response_type == Messages.failure):
            self._handle_failure(extra)
        elif(response_type == Messages.order_progress):
            self._handle_order_progress(extra)
        else:
            print(f"Unknown message type received: {response_type}", flush=True)

    def _handle_order_request(self, extra: dict):
        global PRODUCTION_LINE_HAS_FAILURE

        order_request_dto = OrderRequestDTO.from_dict(extra)

        if PRODUCTION_LINE_HAS_FAILURE:
            print(f"Sending failure information...", flush=True)
            self.write_message(json.dumps(build_message(Messages.failure, extra_object={})))
            return

        in_progress = get_orders_by_status(OrderStatus.IN_PROGRESS)
        
        if in_progress:
            order = in_progress[0]
            self.write_message(json.dumps(build_message(Messages.order_response, order)))
            print(f"Order {order.id} in progress.", flush=True)
            return
        
        pending = get_orders_by_status(OrderStatus.PENDING)

        if pending:
            order = pending[0]
            order.status = OrderStatus.IN_PROGRESS
            notify_order_progress(order)
            notify_order_started(order)
            self.write_message(json.dumps(build_message(Messages.order_response, order)))
            print(f"Order {order.id} assigned.", flush=True)
            return

        self.write_message(json.dumps(build_message(Messages.no_orders, extra_object={})))

    def _handle_failure(self, extra: dict):
        global PRODUCTION_LINE_HAS_FAILURE

        failure_dto = FailureDTO.from_dict(extra)
        PRODUCTION_LINE_HAS_FAILURE = True
        notify_order_failed()

        notifier = EmailNotifier()
        notifier.send(
            to_email="admgrac@gmail.com",
            subject="Production Line Alert",
            body="There was a failure on the production line!",
            html="<strong>There was a <span style='color:red;'>failure</span> on the production line!</strong>"
        )

    def _handle_order_progress(self, extra: dict):
        global PRODUCTION_LINE_HAS_FAILURE

        if PRODUCTION_LINE_HAS_FAILURE:
            return

        progress_dto = OrderProgressDTO.from_dict(extra)
        print(f"Parsed ProgressDTO → id={progress_dto.id}, category={progress_dto.progress_category.value}", flush=True)

        order = get_order(progress_dto.id)

        if not order:
            print(f"Order with id={progress_dto.id} not found.", flush=True)
            return

        if order.status != OrderStatus.IN_PROGRESS:
            return

        if progress_dto.progress_category == ProductCategory.A:
            order.progress_a += 1
            print(f"Updated progress_a to {order.progress_a}/{order.quantity_a}", flush=True)
        elif progress_dto.progress_category == ProductCategory.B:
            order.progress_b += 1
            print(f"Updated progress_b to {order.progress_b}/{order.quantity_b}", flush=True)
        elif progress_dto.progress_category == ProductCategory.C:
            order.progress_c += 1
            print(f"Updated progress_c to {order.progress_c}/{order.quantity_c}", flush=True)

        notify_order_progress(order)

        if (
            order.progress_a >= order.quantity_a and
            order.progress_b >= order.quantity_b and
            order.progress_c >= order.quantity_c
        ):
            order.status = OrderStatus.COMPLETED
            print(f"Order {order.id} completed.", flush=True)
            notify_order_progress(order)
            notify_order_completed(order)
    
def make_app():
    return tornado.web.Application(
        [
            (Routes.login, LoginHandler),
            (Routes.logout, LogoutHandler),
            (Routes.home, HomeHandler),
            (WS_ENDPOINT, ClientWebSocketHandler),
            (UI_ENDPOINT, UIWebSocketHandler),
        ],
        cookie_secret="__SECRET_KEY__",
        login_url=Routes.login,
        template_path=TEMPLATES,
        debug=True
    )

async def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else SERVER_PORT
    address = sys.argv[2] if len(sys.argv) > 2 else SERVER_HOST

    app = make_app()
    app.listen(port=port, address=address)

    print(f"Server is running on http://{address}:{port}/")

    shutdown_event = asyncio.Event()

    def handle_signal():
        print("\nShutting down...")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, handle_signal)
    loop.add_signal_handler(signal.SIGTERM, handle_signal)

    await shutdown_event.wait()

    print("Server stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user.", flush=True)
    finally:
        print("Saving orders to disk...", flush=True)
        save_orders_to_file()
        print("Done.", flush=True)