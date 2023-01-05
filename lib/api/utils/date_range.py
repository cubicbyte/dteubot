import logging
from datetime import date, timedelta

logger = logging.getLogger(__name__)

def get_date_range(d: date) -> list[date]:
    """Returns the first and last day of the week of the given date"""

    if logger.level > 10:
        logger.debug('Getting date range for %s' % d.isoformat())
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)

    return start, end
