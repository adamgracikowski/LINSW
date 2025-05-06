from dataclasses import dataclass, asdict
import json

from enums import *

@dataclass
class OrderRequestDTO:
    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_str: str) -> "OrderRequestDTO":
        data = json.loads(json_str)
        return OrderRequestDTO(**data)

    @staticmethod
    def from_dict(data: dict) -> "OrderRequestDTO":
        return OrderRequestDTO(**data)

@dataclass
class OrderProgressDTO:
    id: str
    progress_category: ProductCategory

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "progress_category": self.progress_category.value
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_str: str) -> "OrderProgressDTO":
        data = json.loads(json_str)
        data['progress_category'] = ProductCategory(data['progress_category'])
        return OrderProgressDTO(**data)

    @staticmethod
    def from_dict(data: dict) -> "OrderProgressDTO":
        data['progress_category'] = ProductCategory(data['progress_category'])
        return OrderProgressDTO(**data)


@dataclass
class OrderResponseDTO:
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
    def from_dict(data: dict) -> "OrderResponseDTO":
        data['status'] = OrderStatus(data['status'])
        return OrderResponseDTO(**data)

    @staticmethod
    def from_json(json_str: str) -> "OrderResponseDTO":
        data = json.loads(json_str)
        return OrderResponseDTO.from_dict(data)


@dataclass
class FailureDTO:
    id: int

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data: dict) -> "FailureDTO":
        return FailureDTO(**data)

    @staticmethod
    def from_json(json_str: str) -> "FailureDTO":
        data = json.loads(json_str)
        return FailureDTO.from_dict(data)