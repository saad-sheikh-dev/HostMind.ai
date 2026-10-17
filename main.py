import asyncio
import random
from database.mock_db import db
from agents.host_agent import HostAgent
from agents.shelf_agent import ShelfAgent
from agents.expiry_agent import ExpiryAgent
from agents.billing_agent import BillingAgent
from agents.cleaning_agent import CleaningAgent
from utils.logger import logger

async def simulation_loop():
    shelf_agent = ShelfAgent()
    expiry_agent = ExpiryAgent()
    billing_agent = BillingAgent()
    cleaning_agent = CleaningAgent()
    
    host = HostAgent([shelf_agent, expiry_agent, billing_agent, cleaning_agent])

    logger.info("Initializing HostMind Autonomous Supermarket Prototype...")
    logger.info("Setup complete. Starting simulation loop. (Ctrl+C to stop)")

    try:
        for cycle in range(1, 6):
            logger.info(f"\n=== SIMULATION CYCLE {cycle} ===")
            db.billing_queue_length = random.randint(0, 10)
            db.mismatch_detected = random.choice([True, False]) if cycle == 3 else False
            db.spill_event = random.choice([True, False]) if cycle == 2 else False
            
            proposed_tasks = await host.orchestrate(db)
            
            discount_tasks = [t for t in proposed_tasks if t.type == "discount"]
            if discount_tasks:
                await expiry_agent.apply_discounts(discount_tasks)

            await asyncio.sleep(2)
            
        logger.info("\nSimulation completed successfully.")

    except KeyboardInterrupt:
        logger.info("Simulation stopped by user.")
    except Exception as e:
        logger.error(f"Critical Simulation Error: {e}")

if __name__ == "__main__":
    asyncio.run(simulation_loop())