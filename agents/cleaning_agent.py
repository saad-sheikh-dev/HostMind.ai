import asyncio
import uuid
from models.schemas import Task, TaskType, Priority
from database.mock_db import db
from utils.logger import logger

class CleaningAgent:
    async def check_cleaning_needs(self) -> list[Task]:
        tasks = []
        if db.spill_event:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                type=TaskType.CLEANING,
                priority=Priority.CRITICAL,
                description="URGENT: Spill detected in aisle 4."
            ))
        tasks.append(Task(
            id=str(uuid.uuid4()),
            type=TaskType.CLEANING,
            priority=Priority.LOW,
            description="Routine floor buffing scheduled."
        ))
        return tasks