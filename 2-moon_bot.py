"""A little daily moon report for Monterrey, Mexico."""

from __future__ import annotations

import os
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import ephem

ZONE = ZoneInfo("America/Monterrey")
LATITUDE = "25.6866"
LONGITUDE = "-100.3161"
PHASES = (
    ("New Moon", "🌑"),
    ("Waxing Crescent", "🌒"),
    ("First Quarter", "🌓"),
    ("Waxing Gibbous", "🌔"),
    ("Full Moon", "🌕"),
    ("Waning Gibbous", "🌖"),
    ("Last Quarter", "🌗"),
    ("Waning Crescent", "🌘"),
)


def utc_datetime(ephem_date: ephem.Date) -> datetime:
    """PyEphem dates are UTC; attach tzinfo before converting to local time."""
    return ephem.Date(ephem_date).datetime().replace(tzinfo=timezone.utc)


def phase(now: datetime) -> tuple[str, str, int]:
    moment = ephem.Date(now.astimezone(timezone.utc))
    previous = ephem.previous_new_moon(moment)
    following = ephem.next_new_moon(moment)
    fraction = (moment - previous) / (following - previous)
    index = int(fraction * 8 + 0.5) % 8
    moon = ephem.Moon(moment)
    label, emoji = PHASES[index]
    return label, emoji, round(moon.phase)


def moonrise_today(now: datetime) -> datetime | None:
    """Find a rise during today's local midnight-to-midnight interval."""
    local_day = now.astimezone(ZONE).date()
    start = datetime.combine(local_day, time.min, ZONE)
    end = datetime.combine(local_day + timedelta(days=1), time.min, ZONE)
    observer = ephem.Observer()
    observer.lat = LATITUDE
    observer.lon = LONGITUDE
    observer.date = ephem.Date(start.astimezone(timezone.utc))
    try:
        rising = utc_datetime(observer.next_rising(ephem.Moon()))
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        return None
    return rising.astimezone(ZONE) if rising < end.astimezone(timezone.utc) else None


def report(now: datetime) -> str:
    if now.tzinfo is None:
        raise ValueError("Pass a timezone-aware datetime")
    local = now.astimezone(ZONE)
    label, emoji, illuminated = phase(now)
    rising = moonrise_today(now)
    rise_text = rising.strftime("%I:%M %p").lstrip("0") if rising else "No moonrise today"
    full = utc_datetime(ephem.next_full_moon(ephem.Date(now.astimezone(timezone.utc)))).astimezone(ZONE)
    days = (full.date() - local.date()).days
    lines = [
        f"# Moon over Monterrey - {local:%B} {local.day}, {local.year}",
        "",
        f"{emoji} **{label}** ({illuminated}% illuminated)",
        f"🌙 **Moonrise today:** {rise_text} (Monterrey time)",
        f"🌕 **Next full moon:** {full:%B} {full.day} at {full.strftime('%I:%M %p').lstrip('0')} (Monterrey time)",
    ]
    if 1 <= days <= 2:
        lines += ["", f"✨ Heads-up: full moon in {days} day{'s' if days != 1 else ''}!"]
    elif days == 0:
        lines += ["", "✨ Full moon today!"]
    return "\n".join(lines) + "\n"


def main() -> None:
    text = report(datetime.now(timezone.utc))
    print(text, end="")
    if summary_file := os.environ.get("GITHUB_STEP_SUMMARY"):
        Path(summary_file).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
