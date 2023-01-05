from datetime import datetime, timedelta

def get_date_range(date: datetime) -> list[datetime]:
    """Returns the first and last day of the week of the given date"""

    week_start = date - timedelta(days=date.weekday())
    week_end = week_start + timedelta(days=6)

    return week_start, week_end