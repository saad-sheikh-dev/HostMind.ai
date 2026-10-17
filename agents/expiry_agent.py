import asyncio
import uuid
from datetime import datetime
from models.schemas import Task, TaskType, Priority
from database.mock_db import db
from utils.logger import logger

class ExpiryAgent:
    async def check_expiry(self) -> list[Task]:
        tasks = []
        now = datetime.now()
        for item in db.items:
            expiry_days = (item.expiry_date - now).days
            if 0 <= expiry_days <= 3:
                discount_percent = min(50.0, 10.0 * (4 - expiry_days))
                discount_percent = max(0.0, discount_percent)
                
                if discount_percent > 0:
                    tasks.append(Task(
                        id=str(uuid.uuid4()),
                        type=TaskType.DISCOUNT,
                        priority=Priority.MEDIUM,
                        description=f"Apply {discount_percent}% discount to {item.name} (Expires in {expiry_days} days)",
                        target_id=item.id
                    ))
        return tasks

    async def apply_discounts(self, tasks: list[Task]):
        for task in tasks:
            item = next((i for i in db.items if i.id == task.target_id), None)
            if item:
                expiry_days = (item.expiry_date - datetime.now()).days
                discount_percent = max(0.0, min(50.0, 10.0 * (4 - expiry_days)))
                item.price = round(item.price * (1 - (discount_percent / 100)), 2)
                logger.info(f"[ExpiryAgent] Applied {discount_percent}% discount to {item.name}. New price: {item.price}")