import json

class Messages:
    order_request = 'order_request'
    order_response = 'order_response'
    no_orders = 'no_orders'
    order_progress = 'order_progress'
    failure = 'failure'
    order_retry = 'order_retry'
    new_order = 'new_order'
    init_ui = 'init_ui'
    order_started = 'order_started'
    order_completed = 'order_completed'
    order_failed = 'order_failed'
    clear_failure = 'clear_failure'

def build_message(message_type: str, extra_object=None) -> dict:
    if extra_object is None:
        extra = {}
    elif hasattr(extra_object, "to_dict"):
        extra = extra_object.to_dict()
    elif isinstance(extra_object, dict):
        extra = extra_object
    else:
        raise ValueError(f"Cannot serialize extra_object of type {type(extra_object)}")
    
    return {
        "type": message_type,
        "extra": extra
    }

def extract_type_and_extra(response_raw):
    response_data = json.loads(response_raw)
    response_type = response_data.get("type")
    extra = response_data.get("extra")
    return response_type, extra

async def receive_message(websocket):
    response_raw = await websocket.recv()
    print("Received from server:", response_raw, flush=True)
    return extract_type_and_extra(response_raw)

def broadcast_message(clients, message):
    raw = json.dumps(message)
    for ws in list(clients):
        try:
            ws.write_message(raw)
        except Exception:
            clients.discard(ws)