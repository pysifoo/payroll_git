from sqlmodel import Session
from datetime import datetime
from decimal import Decimal

from app.database import engine, create_db_and_tables
from app.models import Employee, Contract, WorkShift


def seed_data():

    create_db_and_tables()
    
    with Session(engine) as session:
        jimmy = Employee(has_tax_relief=True)
        session.add(jimmy)
        session.commit()
        session.refresh(jimmy)

        contract = Contract(
            employee_id=jimmy.id,
            contract_type="UoP",
            hourly_rate=Decimal("29.48"),
            )
        session.add(contract)

        shifts = [
            WorkShift(
                employee_id=jimmy.id,
                start_time=datetime(2026, 9, 22, 22, 0),
                end_time=datetime(2026, 9, 23, 6, 0),
                ),
            WorkShift(
                employee_id=jimmy.id,
                start_time=datetime(2026, 9, 18, 22, 0),
                end_time=datetime(2026, 9, 19, 6, 0)
                )
            ]
        session.add_all(shifts)
        session.commit()
        print("The Data was saved in the database")

if __name__ == "__main__":
    seed_data()
                    
