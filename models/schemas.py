from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskType(str, Enum):
    REFILL = "refill"
    DISCOUNT = "discount"
    CLEANING = "cleaning"
    BILLING_CHECK = "billing_check"
    GENERAL = "general"

class Item(BaseModel):
    id: str
    name: str
    price: float
    quantity: int
    capacity: int
    expiry_date: datetime

class Task(BaseModel):
    id: str
    type: TaskType
    priority: Priority
    description: str
    target_id: Optional[str] = None

class Alert(BaseModel):
    level: str
    message: str

class Transaction(BaseModel):
    id: str
    items: List[str]
    total: float
    timestamp: datetime