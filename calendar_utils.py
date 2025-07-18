import io
from ics import Calendar, Event
from datetime import datetime, timedelta
from flask import send_file

# Map days to weekday numbers (used for weekly recurrence)
DAY_MAP = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
}

# Fallback dates based on term name
TERM_RANGES = {
    "Winter": ("Jan 1", "Apr 30"),
    "Spring": ("May 1", "Aug 31"),
    "Fall":   ("Sep 1", "Dec 31"),
}

def parse_term_span(term_str, term_span):
    if term_span:
        start_str, end_str = term_span.split(" - ")
        # Extract year from term (e.g. "Winter 2025")
        term_parts = term_str.strip().split()
        if len(term_parts) >= 2:
            year = term_parts[1]
        else:
            raise ValueError(f"Invalid term format: {term_str}")
    else:
        # Also extract year from term
        term_parts = term_str.strip().split()
        if len(term_parts) >= 2:
            term_name = term_parts[0]
            year = term_parts[1]
            start_str, end_str = TERM_RANGES.get(term_name)
        else:
            raise ValueError(f"Invalid term format: {term_str}")

    start_date = datetime.strptime(start_str + " " + year, "%b %d %Y")
    end_date = datetime.strptime(end_str + " " + year, "%b %d %Y")
    return start_date, end_date



def parse_days(day_str):
    return [d.strip() for d in day_str.split(",") if d.strip() in DAY_MAP]


def parse_time(time_str):
    return datetime.strptime(time_str, "%I:%M%p").time()


def make_calendar(info_list):
    calendar = Calendar()

    for info in info_list:
        # Get start and end date of term
        start_date, end_date = parse_term_span(info["term"], info["term_span"])

        # Days, times, and location
        lecture_days = parse_days(info["lecture_days"])
        start_time = parse_time(info["start_time"])
        end_time = parse_time(info["end_time"])

        for weekday in lecture_days:
            day_offset = (DAY_MAP[weekday] - start_date.weekday()) % 7
            first_class_date = start_date + timedelta(days=day_offset)

            start_dt = datetime.combine(first_class_date, start_time)
            end_dt = datetime.combine(first_class_date, end_time)
            until_dt = datetime.combine(end_date, end_time)

            # Create recurring weekly event
            event = Event()
            event.name = f"{info['course_code']} ({info['lecture_type']}) @ {info['location']}"
            event.begin = start_dt
            event.end = end_dt
            event.location = info['location']
            event.description = info['course_name']
            event.rrule = {
                "freq": "weekly",
                "until": until_dt
            }

            calendar.events.add(event)

    # Return downloadable calendar file
    file = io.StringIO(calendar.serialize())
    return send_file(
        io.BytesIO(file.getvalue().encode()),
        mimetype="text/calendar",
        as_attachment=True,
        download_name="course_schedule.ics"
    )
