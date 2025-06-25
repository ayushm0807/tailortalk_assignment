from gcalendar.google_calender import check_availability, create_event

slot = "2025-06-29T15:00:00+05:30"

if check_availability(slot):
    create_event(slot, "Test Event", "someone@gmail.com")
else:
    print("❌ Slot already booked.")
