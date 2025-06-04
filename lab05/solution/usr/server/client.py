#!/usr/bin/python3

import asyncio
import websockets
import json
import time
import os
import sys

from config import *
from messages import *
from dtos import *
from enums import *
from hardware import *

PRODUCTION_LINE_HAS_FAILURE = False

async def process_order(order_response: OrderResponseDTO, websocket, hardware_module: HardwareModule):
    global PRODUCTION_LINE_HAS_FAILURE

    print(f"Processing order: {order_response.name}", flush=True)
    print(f"Press A, B or C to report progress.", flush=True)
    print(f"Press F to report FAILURE and abort the order.", flush=True)

    progress_counts = {
        ProductCategory.A: order_response.progress_a,
        ProductCategory.B: order_response.progress_b,
        ProductCategory.C: order_response.progress_c
    }

    max_quantities = {
        ProductCategory.A: order_response.quantity_a,
        ProductCategory.B: order_response.quantity_b,
        ProductCategory.C: order_response.quantity_c
    }

    while True:
        category = await hardware_module.detect_progress_category()

        if category is None:
            continue

        if PRODUCTION_LINE_HAS_FAILURE:
            return

        if category == ProductCategory.F:
            print(f"PRODUCTION LINE FAILURE!", flush=True)
            PRODUCTION_LINE_HAS_FAILURE = True
            failure_dto = FailureDTO(id=order_response.id)
            failure_message = build_message(Messages.failure, failure_dto)
            await websocket.send(json.dumps(failure_message))
            return

        if progress_counts[category] >= max_quantities[category]:
            print(f"All units for category {category.value} are already reported.", flush=True)
            continue

        progress_dto = OrderProgressDTO(id=order_response.id, progress_category=category)
        progress_message = build_message(Messages.order_progress, progress_dto)

        await websocket.send(json.dumps(progress_message))
        progress_counts[category] += 1

        print(f"Reported progress for category {category.value} ({progress_counts[category]}/{max_quantities[category]}).", flush=True)

        if all(progress_counts[cat] >= max_quantities[cat] for cat in [ProductCategory.A, ProductCategory.B, ProductCategory.C]):
            print(f"Order {order_response.name} completed!", flush=True)
            break

async def client(hardware):
    global PRODUCTION_LINE_HAS_FAILURE
    uri = f"ws://{SERVER_HOST}:{SERVER_PORT}{WS_ENDPOINT}"
    try:   
        async with websockets.connect(uri) as websocket:
            waiting_for_retry = False

            while True:
                if not waiting_for_retry:
                    order_request_message = build_message(Messages.order_request, OrderRequestDTO())
                    await websocket.send(json.dumps(order_request_message))
                
                response_type, extra = await receive_message(websocket)

                if response_type == Messages.order_response:
                    hardware.turn_off_all_diodes()
                    hardware.set_diode_state(color=DiodeColors.GREEN, on=True)
                    await process_order(OrderResponseDTO.from_dict(extra), websocket, hardware)
                    hardware.turn_off_all_diodes()
                    hardware.set_diode_state(color=DiodeColors.YELLOW, on=True)
                    waiting_for_retry = False
                elif response_type in [Messages.no_orders, Messages.failure]:
                    hardware.turn_off_all_diodes()
                    color = DiodeColors.YELLOW if response_type == Messages.no_orders else DiodeColors.RED
                    hardware.set_diode_state(color=color, on=True)
                    waiting_for_retry = True
                    if response_type == Messages.failure:
                        PRODUCTION_LINE_HAS_FAILURE = True
                elif response_type == Messages.clear_failure:
                    hardware.turn_off_all_diodes()
                    hardware.set_diode_state(color=DiodeColors.YELLOW, on=True)
                    waiting_for_retry = False
                    PRODUCTION_LINE_HAS_FAILURE = False
                elif response_type == Messages.order_retry:
                    print("Retrying order request...", flush=True)
                    waiting_for_retry = False
                else:
                    print(f"Unknown message type received: {response_type}", flush=True)
    except ConnectionRefusedError:
        print(f"Could not connect to the server at {uri}.", flush=True)
        print("Please make sure the server is running.", flush=True)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", flush=True)
    finally:
        hardware.dispose()

async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "gpio":
        hardware = GPIOModule(
            progress_pins={
                ProductCategory.A: BUTTON_A_PIN,
                ProductCategory.B: BUTTON_B_PIN,
                ProductCategory.C: BUTTON_C_PIN
            },
            failure_pin=BUTTON_FAILURE_PIN,
            diode_pins={
                DiodeColors.RED: LED_RED_PIN,
                DiodeColors.GREEN: LED_GREEN_PIN,
                DiodeColors.YELLOW: LED_YELLOW_PIN
            }
        )
        await hardware.start_polling()
    else:
        hardware = KeyboardModule()

    try:
        await client(hardware)
    finally:
        hardware.dispose()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient terminated by user (Ctrl+C). Goodbye!", flush=True)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", flush=True)