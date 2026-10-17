import asyncio
from models.schemas import Task, Priority, TaskType
from utils.logger import logger

class GemmaSimulator:
    """Simulates LLM-based natural language summaries."""
    @staticmethod
    async def summarize_status(tasks: list[Task]) -> str:
        if not tasks:
            return "System Status: All clear. No immediate actions required."
        critical_count = len([t for t in tasks if t.priority == Priority.CRITICAL])
        return f"HostMind Summary: {len(tasks)} tasks pending. {critical_count} critical issues require immediate attention."

class HostAgent:
    def __init__(self, workers):
        self.workers = workers
        self.gemma = GemmaSimulator()

    async def orchestrate(self, db):
        logger.info("--- HostAgent: Starting Orchestration Cycle ---")
        all_proposed_tasks = []

        for worker in self.workers:
            try:
                if hasattr(worker, 'scan_and_refill'):
                    wt = await worker.scan_and_refill()
                elif hasattr(worker, 'check_expiry'):
                    wt = await worker.check_expiry()
                elif hasattr(worker, 'monitor_billing'):
                    wt = await worker.monitor_billing()
                else:
                    wt = await worker.check_cleaning_needs()
                all_proposed_tasks.extend(wt)
            except Exception as e:
                logger.error(f"Error polling worker {worker.__class__.__name__}: {e}")

        priority_map = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
        all_proposed_tasks.sort(key=lambda x: priority_map[x.priority])

        summary = await self.gemma.summarize_status(all_proposed_tasks)
        logger.info(f"[Gemma-Summary] {summary}")

        for task in all_proposed_tasks:
            logger.info(f"[Host] Dispatching Task [{task.priority.value.upper()}]: {task.description}")
            
            if task.type == TaskType.REFILL:
                for item in db.items:
                    if item.id == task.target_id:
                        item.quantity = item.capacity
                        logger.info(f"[Action] Refilled {item.name} to {item.capacity}")
            
            if task.type == TaskType.CLEANING and "Spill" in task.description:
                db.spill_event = False
                logger.info(f"[Action] Spill cleaned up.")

        return all_proposed_tasks