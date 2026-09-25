from datetime import datetime, timedelta
from decimal import Decimal
import holidays

pl_holidays = holidays.Poland()

def analyze_shift(start_time: datetime, end_time: datetime) -> dict:
    """
    Analyze time shift and return report
    - total_hours: Decimal
    - night_hours: Decimal (hours between 22:00 pm till 6:00 am)
    - is_weekend_or_holiday: bool (saturday, sunday, or holiday)
    """
    day_minutes = 0
    night_minutes = 0
    while end_time > start_time:
        if (start_time.hour >= 22 or (
                start_time.hour < 6)):
            night_minutes += 15
        else:
            day_minutes += 15
        start_time += timedelta(minutes=15)

    day_hours = Decimal(day_minutes) / Decimal(60)
    night_hours = Decimal(night_minutes) / Decimal(60)
    total_hours = day_hours + night_hours

    is_weekend = start_time.weekday() in (5,6)
    is_holiday = start_time.date() in pl_holidays

    return {
        "total_hours": total_hours,
        "day_hours": day_hours,
        "night_hours": night_hours,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
    }


if __name__ == "__main__":
    test_wtorek = analyze_shift(
        datetime(2026, 9, 22, 22, 0),
        datetime(2026, 9, 23, 6, 0)
    )
    print("Wtorek:", test_wtorek)

    test_sobota = analyze_shift(
        datetime(2026, 9, 19, 22, 0),
        datetime(2026, 9, 20, 6, 0)
    )
    print("Sobota:", test_sobota)