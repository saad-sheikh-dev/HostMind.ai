
from pathlib import Path
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMMA_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMMA_API_KEY missing. Check D:\\gemma4-hackathon\\.env"
    )

client = genai.Client(api_key=api_key)

project = Path("hostmind")
project.mkdir(exist_ok=True)

prompt = r"""
Build HostMind, an executable Python prototype for autonomous
supermarket operations using a hierarchical multi-agent architecture.

Create these files:
main.py
agents/host_agent.py
agents/shelf_agent.py
agents/expiry_agent.py
agents/billing_agent.py
agents/cleaning_agent.py
models/schemas.py
database/mock_db.py
utils/logger.py

Requirements:
- Use Python asyncio for event-driven orchestration.
- Use Pydantic for Item, Transaction, Task, and Alert schemas.
- HOST is the central orchestrator; worker agents follow HOST directives.
- Shelf agent triggers refills at or below 15% stock capacity.
- Forecast demand using sample historical weekend sales.
- Expiry agent applies:
  discount = min(50, 10 * (4 - expiry_days))
  for items expiring within 3 days, with no negative discounts.
- Billing agent detects mismatches and flags queue lengths above 5.
- Cleaning agent reacts to simulated spill events and schedules.
- Include a mock dataset, logging, priorities, error handling,
  and a runnable demo.
- Use deterministic Python rules for critical pricing and stock logic.
- Use Gemma only for optional natural-language summaries or decisions;
  never let model output directly execute physical actions.
- Use safe mock actions only; no real POS or pricing changes.
- Generate complete files, not explanations or placeholders.
- Keep dependencies minimal and document setup instructions.

Return one JSON object only:
{
  "files": [
    {"path": "main.py", "content": "..."},
    {"path": "agents/host_agent.py", "content": "..."}
  ]
}
Escape newlines and quotes correctly in JSON file contents.
Include all required files in the response.
"""

response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents=prompt,
)

print(response.text)
print("\nGemma response received.")
print("Next: save the generated files into the hostmind folder.")
