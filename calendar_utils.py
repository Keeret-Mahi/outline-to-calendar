"""
calendar_utils.py  (manual .ics builder, no external libs)
"""

import io
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from flask import send_file

# ──────────────── Weekday helpers ─────────────────
DAY_INDEX = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3,
             "Fri": 4, "Sat": 5, "Sun": 6}
DAY_CODE  = {v: k[:2].upper() for k, v in DAY_INDEX.items()}  # 0→MO, 1→TU …

def _byday(names):
    """['Tue','Thu'] → 'TU,TH'"""
    return ",".join(DAY_CODE[DAY_INDEX[n]] for n in names)

# ──────────────── Term fallback ranges ────────────
TERM_RANGES = {
    "Winter": ("Jan 1", "Apr 30"),
    "Spring": ("May 1", "Aug 31"),
    "Fall":   ("Sep 1", "Dec 31"),
}

def parse_term_span(term: str, span: Optional[str]):
    """
    "Fall 2020", "Sep 8 - Dec 7" → (start_dt, end_dt)  naive datetimes
    """
    name, year = term.split()
    if span:
        s, e = [p.strip() for p in span.split(" - ")]
    else:
        s, e = TERM_RANGES[name]
    return (
        datetime.strptime(f"{s} {year}", "%b %d %Y"),
        datetime.strptime(f"{e} {year}", "%b %d %Y"),
    )

def parse_days(s: str):
    return [d.strip() for d in s.split(",") if d.strip() in DAY_INDEX]

def parse_time(s: str):
    return datetime.strptime(s, "%I:%M%p").time()

# ──────────────── VEVENT builder ──────────────────
TZID = "America/Toronto"

def _format_dt(dt: datetime, with_tz=True):
    """2020‑09‑08 14:30 -> '20200908T143000' (local)"""
    fmt = "%Y%m%dT%H%M%S"
    return dt.strftime(fmt) if with_tz else dt.strftime(fmt + "Z")

def _vevent(info: Dict) -> str:
    """Return VEVENT string for one course/section."""
    term_start, term_end = parse_term_span(info["term"], info["term_span"])
    days       = parse_days(info["lecture_days"])
    start_time = parse_time(info["start_time"])
    end_time   = parse_time(info["end_time"])

    # First meeting date = earliest day in `days` on/after term_start
    offsets = [(DAY_INDEX[d] - term_start.weekday()) % 7 for d in days]
    first   = term_start + timedelta(days=min(offsets))

    dt_start = datetime.combine(first, start_time)
    dt_end   = datetime.combine(first, end_time)
    until_dt = datetime.combine(term_end.date(), end_time)

    uid      = uuid.uuid4().hex + "@outline2ics"
    stamp    = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{stamp}",
        f"SUMMARY:{info['course_code']} ({info['lecture_type']}) @ {info['location']}",
        f"DTSTART;TZID={TZID}:{_format_dt(dt_start)}",
        f"DTEND;TZID={TZID}:{_format_dt(dt_end)}",
        f"RRULE:FREQ=WEEKLY;BYDAY={_byday(days)};UNTIL={_format_dt(until_dt, False)}",
        f"LOCATION:{info['location']}",
        f"DESCRIPTION:{info['course_name']}",
        "END:VEVENT",
    ]
    return "\n".join(lines)

# ──────────────── main entry ─────────────────────
def make_calendar(info_list: List[Dict]):
    """
    Build VCALENDAR from a list of section dicts (same schema you already use)
    and return it via Flask send_file().
    """
    parts = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Outline‑to‑ICS//EN",
        "CALSCALE:GREGORIAN",
        f"X-WR-TIMEZONE:{TZID}",
    ]
    for info in info_list:
        parts.append(_vevent(info))
    parts.append("END:VCALENDAR")

    ics_text = "\n".join(parts) + "\n"
    buf = io.BytesIO(ics_text.encode("utf-8"))
    return send_file(
        buf,
        mimetype="text/calendar",
        as_attachment=True,
        download_name="course_schedule.ics"
    )
