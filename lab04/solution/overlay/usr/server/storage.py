import os
import json
from typing import Dict, Optional, List
from dataclasses import asdict

from models import *
from enums import *

_orders: Dict[int, Order] = {}
_next_order_id: int = 1

_loaded = False
_STORE_FILE = "orders.json"

def _ensure_loaded():
    global _loaded, _orders, _next_order_id
    if _loaded:
        return
    _loaded = True
    if os.path.exists(_STORE_FILE):
        with open(_STORE_FILE, "r") as f:
            data_list = json.load(f)
        for item in data_list:
            order = Order.from_dict(item)
            _orders[order.id] = order
        if _orders:
            _next_order_id = max(_orders.keys()) + 1

def save_orders_to_file():
    dirpath = os.path.dirname(_STORE_FILE)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(_STORE_FILE, "w") as f:
        json.dump([order.to_dict() for order in _orders.values()], f, indent=2)

def add_order(
    name: str,
    quantity_a: int,
    quantity_b: int,
    quantity_c: int,
) -> Order:
    global _next_order_id
    _ensure_loaded()
    order = Order(
        id=_next_order_id,
        name=name,
        quantity_a=quantity_a,
        quantity_b=quantity_b,
        quantity_c=quantity_c,
        progress_a=0,
        progress_b=0,
        progress_c=0,
        status=OrderStatus.PENDING
    )
    _orders[_next_order_id] = order
    _next_order_id += 1
    save_orders_to_file()
    return order

def get_order(order_id: int) -> Optional[Order]:
    _ensure_loaded()
    return _orders.get(order_id)

def get_orders_by_status(
    status: Optional[OrderStatus] = None
) -> List[Order]:
    _ensure_loaded()
    if status is None:
        return list(_orders.values())
    return [order for order in _orders.values() if order.status == status]