from dataclasses import dataclass, asdict
import json
from typing import List

from enums import *

@dataclass
class Order:
    id: int
    name: str
    quantity_a: int
    quantity_b: int
    quantity_c: int
    progress_a: int
    progress_b: int
    progress_c: int
    status: OrderStatus

    def to_dict(self) -> dict:
        data = asdict(self)
        data['status'] = self.status.value
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def list_to_json(orders: List["Order"]) -> str:
        return json.dumps([order.to_dict() for order in orders])

    @staticmethod
    def from_dict(data: dict) -> "Order":
        data['status'] = OrderStatus(data['status'])
        return Order(**data)

    @staticmethod
    def list_from_json(json_str: str) -> List["Order"]:
        data_list = json.loads(json_str)
        return [Order.from_dict(item) for item in data_list]