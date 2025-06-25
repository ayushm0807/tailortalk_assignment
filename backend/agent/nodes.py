import re
import dateparser
from datetime import datetime, timedelta
from typing import TypedDict

from backend.gcalendar.google_calender import check_availability, create_event

class BookingState(TypedDict):
    input: str
    session_id: str
    slot: str
    available: bool
    message: str

def greet(state: BookingState) -> BookingState:
    if not state.get("message"):
        state["message"] = "👋 Hello! I can help you book a slot."
    return state

def ask_slot_info(state: BookingState) -> BookingState:
    msg = state["input"]
    print("📨 User message:", msg)

    date = dateparser.parse(
        msg, 
        settings={"PREFER_DATES_FROM": "future", "RELATIVE_BASE": datetime.now()}
    )

    if not date:
        state["slot"] = "UNKNOWN"
        state["message"] = "❌ I couldn't understand the date. Could you rephrase?"
        return state

    print("📅 Parsed date:", date)

    # Extract time range, e.g. "3 to 5 PM"
    time_match = re.search(r'(\d{1,2})\s*[-to]+\s*(\d{1,2})\s*(AM|PM|am|pm)?', msg)
    possible_slots = []

    if time_match:
        start_hour = int(time_match.group(1))
        end_hour = int(time_match.group(2))
        period = time_match.group(3) or "PM"

        if "pm" in period.lower() and start_hour < 12:
            start_hour += 12
            end_hour += 12

        for hour in range(start_hour, end_hour):
            slot_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            iso = slot_time.isoformat()
            if check_availability(iso):
                state["slot"] = iso
                state["message"] = f"✅ Slot available at {slot_time.strftime('%I:%M %p on %A, %B %d')}."
                return state
    else:
        # No specific time? Try common options: 3 PM, 4 PM, 5 PM
        for hour in [15, 16, 17]:
            slot_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            iso = slot_time.isoformat()
            print(f"🔍 Trying default slot: {iso}")
            if check_availability(iso):
                state["slot"] = iso
                state["message"] = f"🕒 Found available slot at {slot_time.strftime('%I:%M %p on %A, %B %d')}."
                return state

    state["slot"] = "UNAVAILABLE"
    state["message"] = "❌ No available slots found for that time."
    return state


def check_calendar(state: BookingState) -> BookingState:
    state["available"] = state["slot"] not in ("UNKNOWN", "UNAVAILABLE")
    return state

def book_slot(state: BookingState) -> BookingState:
    if state["available"]:
        try:
            create_event(
                state["slot"],               # ✅ Corrected positional argument
                "Meeting with AI",           # summary
                "demo@example.com"           # email
            )
            state["message"] = f"✅ Your meeting has been booked for {state['slot']}."
        except Exception as e:
            print("❌ Error during booking:", e)
            state["message"] = "❌ Something went wrong while booking your meeting."
    elif state["slot"] == "UNKNOWN":
        # Keep the message from ask_slot_info
        pass
    else:
        state["message"] = "❌ Could not book a slot as none were available."
    return state
