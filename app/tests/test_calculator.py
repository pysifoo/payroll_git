import pytest
from decimal import Decimal
from app.calculator import calculate_overtime_hours, analyze_shift, calculate_income
from datetime import datetime


@pytest.mark.parametrize("start_time, end_time, expected_result", [
    (
        datetime(2026, 9, 25, 22, 0),
        datetime(2026, 9, 26, 6, 0),
        {
            "total_hours": Decimal("8"),
            "day_hours": Decimal("0"),
            "night_hours": Decimal("8"),
            "is_weekend": False,
            "is_holiday": False
        }
    ),

    (
        datetime(2026, 9, 22, 14, 0),
        datetime(2026, 9, 22, 22, 0),
        {
            "total_hours": Decimal("8"),
            "day_hours": Decimal("8"),
            "night_hours": Decimal("0"),
            "is_weekend": False,
            "is_holiday": False
        }
    ),

    (
        datetime(2026, 9, 20, 22, 0),
        datetime(2026, 9, 21, 6, 0),
        {
            "total_hours": Decimal("8"),
            "day_hours": Decimal("0"),
            "night_hours": Decimal("8"),
            "is_weekend": True,
            "is_holiday": False
        }
    )
])
def test_analyze_shift(start_time, end_time, expected_result):

    result = analyze_shift(start_time, end_time)

    assert result == expected_result

def test_calculate_overtime_hours_regular_day():

    shift_data = {
        "total_hours": Decimal("10"),
        "is_weekend": False,
        "is_holiday": False,
    }

    result = calculate_overtime_hours(shift_data)

    assert result["overtime_hours_50"] == Decimal("2")
    assert result["overtime_hours_100"] == Decimal("0")


def test_calculate_overtime_hours_weeekend():

    shift_data = {
        "total_hours": Decimal("8"),
        "is_weekend": True,
        "is_holiday": False,
        }

    result = calculate_overtime_hours(shift_data)

    assert result["overtime_hours_50"] == Decimal("0")
    assert result["overtime_hours_100"] == Decimal("8")

@pytest.mark.parametrize("shift_data, hourly_rate, expected_result", [
    (
        {
            "total_hours": Decimal("8"),
            "night_hours": Decimal("0"),
            "overtime_hours_50": Decimal("0"),
            "overtime_hours_100": Decimal("0")
        },
        Decimal("30.00"),
        {
            "sum_gross": Decimal("240.00"),
            "sum_net": Decimal("184.80")
        }
    ),
    
    (
        {
            "total_hours": Decimal("8"),
            "night_hours": Decimal("8"),
            "overtime_hours_50": Decimal("0"),
            "overtime_hours_100": Decimal("0")
        },
        Decimal("30.00"),
        {
            "sum_gross": Decimal("288.00"),
            "sum_net": Decimal("221.76")
        }
    ),

    (
        {
            "total_hours": Decimal("10"),
            "night_hours": Decimal("0"),
            "overtime_hours_50": Decimal("2"),
            "overtime_hours_100": Decimal("0")
        },
        Decimal("30.00"),
        {
            "sum_gross": Decimal("330.00"),
            "sum_net": Decimal("254.10")
        }
    )
])
def test_calculate_income(shift_data, hourly_rate, expected_result):

    result = calculate_income(shift_data, hourly_rate)

    assert result == expected_result
