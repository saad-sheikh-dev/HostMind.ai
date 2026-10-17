import asyncio
import uuid
from models.schemas import Task, TaskType, Priority
from database.mock_db import db
from utils.logger import logger

class ShelfAgent:
    async def scan_and_refill(self) -> list[Task]:
        tasks = []
        for item in db.items:
            capacity_pct = (item.quantity / item.capacity)
            forecasted_demand = db.historical_weekend_sales.get(item.name, 0)
            
            if capacity_pct <= 0.15 or item.quantity < forecasted_demand:
                reason = "Low capacity" if capacity_pct <= 0.15 else "Demand forecast mismatch"
                tasks.append(Task(
                    id=str(uuid.uuid4()),
                    type=TaskType.REFILL,
                    priority=Priority.HIGH if capacity_pct < 0.05 else Priority.MEDIUM,
                    description=f"Refill {item.name}: {reason}. Current: {item.quantity}, Target: {item.capacity}",
                    target_id=item.id
                ))
        return tasks