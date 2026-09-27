from sqlmodel import Session, select
from datetime import datetime
from decimal import Decimal

from database import engine
from models import Employee, Contract, WorkShift, MonthlyWorkRecord
from calculator import analyze_shift, calculate_income, calculate_overtime_hours



def generate_monthly_summary(employee_id: int, year: int, month: int):
    with Session(engine) as session:
        statement_contract = select(Contract).where(Contract.employee_id == employee_id)
        contract = session.exec(statement_contract).first()

        if not contract:
            print("This employee doesn\'t have active operative contract")
            return None

        hourly_rate = contract.hourly_rate
        start_of_month = datetime(year, month, 1)

        if month == 12:
            end_of_month = datetime(year +1, 1, 1)
        else:
            end_of_month = datetime(year, month +1, 1)

            statement_shifts = select(WorkShift).where(
                WorkShift.employee_id == employee_id,
                WorkShift.start_time >= start_of_month,
                WorkShift.start_time < end_of_month
                )
            shifts = session.exec(statement_shifts).all()
            shifts_total = {
                "total_hours": Decimal("0"),
                "day_hours": Decimal("0"),
                "night_hours": Decimal("0"),
                "overtime_hours_50": Decimal("0"),
                "overtime_hours_100": Decimal("0"),
            }
            for shift in shifts:
                shift_data = analyze_shift(shift.start_time, shift.end_time)
                overtime = calculate_overtime_hours(shift_data)
                shifts_total["day_hours"] += shift_data["day_hours"]
                shifts_total["night_hours"] += shift_data["night_hours"]
                shifts_total["overtime_hours_50"] += overtime["overtime_hours_50"]
                shifts_total["overtime_hours_100"] += overtime["overtime_hours_100"]
            shifts_total["total_hours"] = shifts_total["day_hours"] + shifts_total["night_hours"]
            income = calculate_income(shifts_total, contract.hourly_rate)

            monthly_record = MonthlyWorkRecord(
                employee_id = employee_id,
                year = year,
                month = month,
                regular_hours = shifts_total["total_hours"],
                night_hours = shifts_total["night_hours"],
                monthly_bonus = Decimal("0"),
                overtime_50_hours = shifts_total["overtime_hours_50"],
                overtime_100_hours = shifts_total["overtime_hours_100"],
                total_gross = income["sum_gross"],
                total_net = income["sum_net"]
                )
            session.add(monthly_record)
            session.commit()
            print(f"The report was successfully saved in database for employee:{employee_id}, year:{year}, month:{month}") 

if __name__ == "__main__":
        monthly_record = generate_monthly_summary(employee_id=2, year=2026, month=9)
        print(monthly_record)
