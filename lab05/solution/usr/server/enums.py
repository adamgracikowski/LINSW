from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ProductCategory(Enum):
    A = "A"
    B = "B"
    C = "C"
    F = "F"

class DiodeColors(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"