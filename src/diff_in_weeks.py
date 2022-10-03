from datetime import timedelta

def diff_in_weeks(d1, d2):
    monday1 = (d1 - timedelta(days=d1.weekday()))
    monday2 = (d2 - timedelta(days=d2.weekday()))

    days = (monday2 - monday1).days

    if days == 0:
        return 0

    return int(days / 7)