from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
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
    current_time = start_time
    while end_time > current_time:
        if (start_time.hour >= 22 or (
                start_time.hour < 6)):
            night_minutes += 15
        else:
            day_minutes += 15
        current_time += timedelta(minutes=15)

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


def calculate_overtime_hours(shift_data: dict) -> dict:
    """
    Calculate overtime per shift and which category it suits then return in dict.
    overtime_50_hours: Decimal (week overtime)
    overtime_100_hours: Decimal (weekend or holidays overtime)
    """
    
    if shift_data["is_holiday"] or shift_data["is_weekend"]:
        return {
            "overtime_hours_50": Decimal("0"),
            "overtime_hours_100": shift_data["total_hours"]
        }
    overtime_50 = Decimal("0")
    if shift_data["total_hours"] > Decimal("8"):
        overtime_50 = shift_data["total_hours"] - Decimal("8")
    return {
        "overtime_hours_50": overtime_50,
        "overtime_hours_100": Decimal("0"),
    }


def calculate_income(shift_data: dict, hourly_rate: Decimal) -> dict:
    """
    Receive dictionary of analyze_shift and hour rate.

    Return dict of figure gross per shift
    """
    base = shift_data["total_hours"] * hourly_rate
    night_hours_base = shift_data["night_hours"] * (hourly_rate * Decimal("0.20"))
    extra_hours = (hourly_rate * Decimal("0.50") * shift_data["overtime_hours_50"]) +\
                  (hourly_rate * shift_data["overtime_hours_100"])

    sum_shift_gross = base + night_hours_base + extra_hours
    sum_shift_net = sum_shift_gross * Decimal("0.77")
    sum_shift_gross = sum_shift_gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    sum_shift_net = sum_shift_net.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return {
        "sum_gross": sum_shift_gross,
        "sum_net": sum_shift_net,
    }

if __name__ == "__main__":
    test_wtorek = analyze_shift(
        datetime(2026, 9, 22, 14, 0),
        datetime(2026, 9, 22, 22, 0)
    )
    print("Wtorek:", test_wtorek)

    test_piatek = analyze_shift(
        datetime(2026, 9, 18, 22, 0),
        datetime(2026, 9, 19, 6, 0)
    )
    print("Piatek:", test_piatek)

    overtime_hours = calculate_overtime_hours(test_piatek)
    shift_data = {**test_piatek, **overtime_hours}
    paycheck = calculate_income(shift_data, Decimal("29.48"))
    print(f"wyplata:{paycheck}")
