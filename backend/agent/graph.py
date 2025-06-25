from langgraph.graph import StateGraph
from typing import TypedDict

from agent.nodes import greet, ask_slot_info, check_calendar, book_slot

# Define schema
class BookingState(TypedDict):
    input: str
    session_id: str
    slot: str
    available: bool
    message: str

# Build the graph
graph = StateGraph(BookingState)

graph.add_node("greet", greet)
graph.add_node("ask_slot_info", ask_slot_info)
graph.add_node("check_calendar", check_calendar)
graph.add_node("book_slot", book_slot)

graph.set_entry_point("greet")
graph.add_edge("greet", "ask_slot_info")
graph.add_edge("ask_slot_info", "check_calendar")
graph.add_edge("check_calendar", "book_slot")

app = graph.compile()

def run_agent(message: str, session_id: str ) -> str:
    state: BookingState = {
        "input": message,
        "session_id": session_id,
        "slot": "",
        "available": False,
        "message": "",
    }

    print("▶️ Initial State:", state)

    for step in app.stream(state):
        print("🔁 Step:", step)
        # Unpack actual inner state (e.g. from {"book_slot": {...}})
        state = list(step.values())[0]  # ✅ this line unpacks the inner dict

    print("✅ Final State:", state)
    return state.get("message", "🤖 I'm not sure what to say.")
