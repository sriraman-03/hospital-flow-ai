
from datetime import datetime

from database import get_connection, get_beds


TIMESTAMP_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d%H:%M:%S",
)


def parse_timestamp(value):
    """Parse supported SQLite timestamp formats safely."""
    if not value:
        return None

    value = str(value).strip()

    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def get_waiting_time_metrics():
    """
    Calculate elapsed time from registration to the first
    recorded transition out of Waiting.

    Patients still waiting are measured up to the current time.
    """
    with get_connection() as conn:
        patients = conn.execute("""
            SELECT patient_code, priority, status
            FROM patients
        """).fetchall()

        events = conn.execute("""
            SELECT patient_code, to_status, event_type, occurred_at
            FROM patient_status_events
            ORDER BY id
        """).fetchall()

    now = datetime.now()
    durations = []
    p1_durations = []
    missing_records = 0

    for patient in patients:
        patient_code = patient["patient_code"]

        patient_events = [
            event for event in events
            if event["patient_code"] == patient_code
        ]

        registration = next(
            (
                parse_timestamp(event["occurred_at"])
                for event in patient_events
                if event["event_type"] == "registration"
                and parse_timestamp(event["occurred_at"]) is not None
            ),
            None,
        )

        if registration is None:
            missing_records += 1
            continue

        first_review = next(
            (
                parse_timestamp(event["occurred_at"])
                for event in patient_events
                if event["to_status"] == "Under Review"
                and parse_timestamp(event["occurred_at"]) is not None
            ),
            None,
        )

        end_time = first_review or now
        seconds = max(0, (end_time - registration).total_seconds())

        # Only count completed waiting intervals in the mean.
        if first_review is not None:
            durations.append(seconds)

            # P1 represents the highest-priority educational flag.
            if patient["priority"] in ("P1", "Critical flag"):
                p1_durations.append(seconds)

    mean_seconds = (
        sum(durations) / len(durations)
        if durations else None
    )

    p1_mean_seconds = (
        sum(p1_durations) / len(p1_durations)
        if p1_durations else None
    )

    return {
        "mean_waiting_minutes": (
            mean_seconds / 60 if mean_seconds is not None else None
        ),
        "p1_mean_waiting_minutes": (
            p1_mean_seconds / 60
            if p1_mean_seconds is not None else None
        ),
        "completed_intervals": len(durations),
        "p1_intervals": len(p1_durations),
        "missing_registration_records": missing_records,
    }


def get_bed_utilisation():
    """Calculate occupancy from the individual bed inventory."""
    beds = get_beds()

    if not beds:
        return {
            "total_beds": 0,
            "occupied_beds": 0,
            "utilisation_percent": None,
        }

    total = len(beds)
    occupied = sum(
        bed["status"] == "Occupied"
        for bed in beds
    )

    return {
        "total_beds": total,
        "occupied_beds": occupied,
        "utilisation_percent": occupied / total * 100,
    }
