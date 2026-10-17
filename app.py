import streamlit as st
import pandas as pd
import asyncio
import time
from datetime import datetime
from database.mock_db import db
from agents.host_agent import HostAgent
from agents.shelf_agent import ShelfAgent
from agents.expiry_agent import ExpiryAgent
from agents.billing_agent import BillingAgent
from agents.cleaning_agent import CleaningAgent
from models.schemas import Priority, TaskType

st.set_page_config(page_title="HostMind - Autonomous Retail Orchestration", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .terminal-box { background-color: #0e1117; color: #00ff66; padding: 15px; border-radius: 5px; font-family: monospace; height: 300px; overflow-y: scroll; border: 1px solid #333; }
    .agent-card { padding: 15px; border-radius: 8px; border: 1px solid #ddd; background-color: #1e2530; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 HostMind: Autonomous Multi-Agent Retail Orchestration")
st.markdown("### *Live Task Orchestration & Agent Activity Feed*")

# Initialize session state
if "shelf_agent" not in st.session_state:
    st.session_state.shelf_agent = ShelfAgent()
    st.session_state.expiry_agent = ExpiryAgent()
    st.session_state.billing_agent = BillingAgent()
    st.session_state.cleaning_agent = CleaningAgent()
    st.session_state.host = HostAgent([
        st.session_state.shelf_agent,
        st.session_state.expiry_agent,
        st.session_state.billing_agent,
        st.session_state.cleaning_agent
    ])
    st.session_state.logs = []
    st.session_state.cycle = 0
    st.session_state.active_tasks = []

# Sidebar Controls
st.sidebar.header("🕹️ Live Simulation Control")

# Placeholder for real-time visual status updates in UI
status_placeholder = st.empty()

if st.sidebar.button("▶ Run Orchestration Cycle", type="primary"):
    st.session_state.cycle += 1
    cycle_num = st.session_state.cycle
    
    # 1. Log Telemetry Scan
    scan_msg = f"[Cycle {cycle_num}] HOST Agent initiated global telemetry scan..."
    st.session_state.logs.append(scan_msg)
    
    status_placeholder.info(f"🔄 [Cycle {cycle_num}] Scanning sensors, inventory levels, and POS feeds...")
    time.sleep(1.0)
    
    # 2. Run backend orchestration to generate tasks
    async def run_live_cycle():
        tasks = await st.session_state.host.orchestrate(db)
        discount_tasks = [t for t in tasks if t.type == TaskType.DISCOUNT]
        if discount_tasks:
            await st.session_state.expiry_agent.apply_discounts(discount_tasks)
        return tasks

    loop_tasks = asyncio.run(run_live_cycle())
    st.session_state.active_tasks = loop_tasks

    status_placeholder.warning(f"⚡ [Cycle {cycle_num}] Evaluating 15% stock thresholds & discount decay algorithms...")
    time.sleep(1.0)

    # 3. Stream each task dispatch line-by-line with smooth 1-second intervals
    for idx, t in enumerate(loop_tasks, 1):
        dispatch_msg = f"[HOST -> Worker] Dispatched [{t.priority.value.upper()}] {t.type.value.upper()}: {t.description}"
        st.session_state.logs.append(dispatch_msg)
        
        status_placeholder.success(f"🚀 **[Step {idx}/{len(loop_tasks)}]** Routing command to `Agent_{t.type.value.capitalize()}` | Priority: `{t.priority.value.upper()}`")
        time.sleep(1.2) # Smooth 1.2 second pause for presentation pacing

    # 4. Completion Log
    complete_msg = f"[Cycle {cycle_num}] All multi-agent directives executed, markdown prices updated, and store audited."
    st.session_state.logs.append(complete_msg)
    
    status_placeholder.success(f"✅ [Cycle {cycle_num}] Orchestration cycle completed successfully!")
    time.sleep(1)
    status_placeholder.empty()
    st.rerun()

if st.sidebar.button("🔄 Reset Store State"):
    db.__init__()
    st.session_state.logs = []
    st.session_state.active_tasks = []
    st.session_state.cycle = 0
    st.rerun()

# --- LIVE WORKFORCE 2x2 GRID ---
st.markdown("### 🤖 Live Sub-Agent Task Tracking Grid")

col1, col2 = st.columns(2)

def get_agent_task_status(task_type_keyword):
    for t in st.session_state.active_tasks:
        if task_type_keyword in t.type.value.lower():
            return t
    return None

with col1:
    # Shelf Agent Card
    shelf_t = get_agent_task_status("refill")
    shelf_status = "🟡 PROCESSING" if shelf_t else "🟢 IDLE / MONITORING"
    shelf_desc = shelf_t.description if shelf_t else "No active refill tasks. SKUs within safe capacity bounds."
    shelf_priority = shelf_t.priority.value.upper() if shelf_t else "NONE"
    
    st.markdown(f"""
    <div class="agent-card">
        <h4>📦 Agent_Shelf (Inventory & Refill)</h4>
        <p><b>Status:</b> {shelf_status}</p>
        <p><b>Current Command:</b> {shelf_desc}</p>
        <p><b>Priority:</b> <code>{shelf_priority}</code></p>
    </div>
    """, unsafe_allow_html=True)

    # Expiry Agent Card
    expiry_t = get_agent_task_status("discount")
    expiry_status = "🟡 PRICING DECAY ACTIVE" if expiry_t else "🟢 IDLE / SCANNING"
    expiry_desc = expiry_t.description if expiry_t else "All batch expiration dates verified. No markdown required."
    expiry_priority = expiry_t.priority.value.upper() if expiry_t else "NONE"

    st.markdown(f"""
    <div class="agent-card">
        <h4>🏷️ Agent_Expiry (Dynamic Markdown)</h4>
        <p><b>Status:</b> {expiry_status}</p>
        <p><b>Current Command:</b> {expiry_desc}</p>
        <p><b>Priority:</b> <code>{expiry_priority}</code></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Billing Agent Card
    billing_t = get_agent_task_status("billing")
    billing_status = "🔴 QUEUE ALERT / AUDIT" if billing_t else "🟢 MONITORING POS"
    billing_desc = billing_t.description if billing_t else "Checkout queues optimal (<= 5 shoppers per lane). No mismatches."
    billing_priority = billing_t.priority.value.upper() if billing_t else "NONE"

    st.markdown(f"""
    <div class="agent-card">
        <h4>💳 Agent_Billing (POS & Queue Audit)</h4>
        <p><b>Status:</b> {billing_status}</p>
        <p><b>Current Command:</b> {billing_desc}</p>
        <p><b>Priority:</b> <code>{billing_priority}</code></p>
    </div>
    """, unsafe_allow_html=True)

    # Cleaning Agent Card
    cleaning_t = get_agent_task_status("cleaning")
    cleaning_status = "🔴 SPILL DETECTED" if cleaning_t and "Spill" in cleaning_t.description else "🟢 ROUTINE BUFFING"
    cleaning_desc = cleaning_t.description if cleaning_t else "No facility alerts reported."
    cleaning_priority = cleaning_t.priority.value.upper() if cleaning_t else "LOW"

    st.markdown(f"""
    <div class="agent-card">
        <h4>🧹 Agent_Cleaning (Facilities)</h4>
        <p><b>Status:</b> {cleaning_status}</p>
        <p><b>Current Command:</b> {cleaning_desc}</p>
        <p><b>Priority:</b> <code>{cleaning_priority}</code></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Telemetry Table
st.markdown("### 📊 Live Store Inventory & Telemetry Table")
item_data = []
for item in db.items:
    expiry_days = (item.expiry_date - datetime.now()).days
    stock_pct = round((item.quantity / item.capacity) * 100, 1)
    item_data.append({
        "SKU": item.name,
        "Price ($)": item.price,
        "Stock Qty": item.quantity,
        "Capacity": item.capacity,
        "Stock Level (%)": f"{stock_pct}%",
        "Expiry (Days)": expiry_days
    })
df_items = pd.DataFrame(item_data)
st.dataframe(df_items, width='stretch')

# Terminal Log View with Clean Line-by-Line HTML Formatting
st.markdown("### 💻 HOST Agent Decision Stream & Real-Time Task Feed")
formatted_logs = "".join([f"<div style='margin-bottom: 6px;'>{log}</div>" for log in st.session_state.logs[-15:]])
terminal_html = f'<div class="terminal-box">{formatted_logs if formatted_logs else "System initialized. Click 'Run Orchestration Cycle' in the sidebar..."}</div>'
st.markdown(terminal_html, unsafe_allow_html=True)