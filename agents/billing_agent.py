import asyncio
import uuid
from models.schemas import Task, TaskType, Priority
from database.mock_db import db
from utils.logger import logger

class BillingAgent:
    async def monitor_billing(self) -> list[Task]:
        tasks = []
        if db.billing_queue_length > 5:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                type=TaskType.BILLING_CHECK,
                priority=Priority.HIGH,
                description=f"High queue detected: {db.billing_queue_length} customers waiting."
            ))
        if db.mismatch_detected:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                type=TaskType.BILLING_CHECK,
                priority=Priority.CRITICAL,
                description="POS Mismatch detected! Verify inventory integrity."
            ))
        return tasks