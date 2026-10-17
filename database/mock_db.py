from datetime import datetime, timedelta
from typing import List, Dict
from models.schemas import Item, Task, Alert

class MockDB:
    def __init__(self):
        self.items: List[Item] = [
            Item(id="it_01", name="Milk", price=3.50, quantity=2, capacity=20, expiry_date=datetime.now() + timedelta(days=2)),
            Item(id="it_02", name="Bread", price=2.00, quantity=15, capacity=20, expiry_date=datetime.now() + timedelta(days=5)),
            Item(id="it_03", name="Eggs", price=4.00, quantity=1, capacity=12, expiry_date=datetime.now() + timedelta(days=1)),
            Item(id="it_04", name="Yogurt", price=1.50, quantity=10, capacity=10, expiry_date=datetime.now() + timedelta(days=10)),
            Item(id="it_05", name="Cheese", price=5.00, quantity=5, capacity=20, expiry_date=datetime.now() + timedelta(days=12)),
        ]
        self.tasks: List[Task] = []
        self.alerts: List[Alert] = []
        self.spill_event: bool = False
        self.billing_queue_length: int = 0
        self.mismatch_detected: bool = False
        
        self.historical_weekend_sales: Dict[str, int] = {
            "Milk": 15,
            "Bread": 12,
            "Eggs": 8,
            "Yogurt": 5,
            "Cheese": 4
        }

    def get_item_by_name(self, name: str) -> Item:
        return next((i for i in self.items if i.name == name), None)

db = MockDB()