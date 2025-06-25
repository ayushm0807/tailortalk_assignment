import os
import json
import base64
from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load .env in local dev
load_dotenv()

# 🔐 Get env variables
CALENDAR_ID = os.getenv("CALENDAR_ID")
GOOGLE_CREDS_BASE64 = os.getenv("GOOGLE_CREDS_BASE64")
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# ✅ Decode base64 credentials from env and build service
creds_dict = json.loads(base64.b64decode(GOOGLE_CREDS_BASE64).decode("utf-8"))
credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
service = build("calendar", "v3", credentials=credentials)

# 🔎 Check slot availability
def check_availability(start_time_iso: str) -> bool:
    try:
        print("🔍 Checking availability for:", start_time_iso)
        
        start_dt = datetime.fromisoformat(start_time_iso).replace(tzinfo=timezone.utc)
        end_dt = start_dt + timedelta(hours=1)

        events = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            maxResults=1,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        is_free = len(events.get("items", [])) == 0
        print("✅ Available:", is_free)
        return is_free

    except Exception as e:
        print("❌ Error checking availability:", e)
        return False

# 📅 Create calendar event
def create_event(start_time_iso: str, summary: str, email: str = ""):
    try:
        start_dt = datetime.fromisoformat(start_time_iso).replace(tzinfo=timezone.utc)
        end_dt = start_dt + timedelta(hours=1)

        event = {
            "summary": summary,
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "Asia/Kolkata"
            }
        }

        service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"📅 Event created at {start_dt.isoformat()}")

    except Exception as e:
        print("❌ Error creating event:", e)
