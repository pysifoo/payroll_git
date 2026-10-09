from fastapi import FastAPI, HTTPException, Depends
from decimal import Decimal
from typing import List
from sqlmodel import select, Session

from app.database import engine
from app.models import Employee, Contract, WorkShift
from app.monthly_summary import generate_monthly_summary, get_existing_summary


app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Working API payroll calculator."} 

def get_session():
    with Session(engine) as session:
        yield session


#Employee endpoints
@app.post("/employees/", response_model=Employee)
def create_employee(employee: Employee, session: Session = Depends(get_session)):
    """
    Add new employee to database
    """
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

@app.get("/employees/", response_model=List[Employee])
def read_employees(session: Session = Depends(get_session)):
    """
    Return list of employees
    """
    employees = session.exec(select(Employee)).all()
    return employees


@app.post("/contracts/", response_model=Contract)
def create_contract(contract: Contract, session: Session = Depends(get_session)):
    """
    Create contract for employee
    """
    session.add(contract)
    session.commit()
    session.refresh(contract)
    return contract

@app.get("/contracts/", response_model=List[Contract])
def read_contracts(session: Session = Depends(get_session)):
    """
    Return list of contracts
    """
    contracts = session.exec(select(Contract)).all()
    return contracts


@app.post("/shifts/", response_model=WorkShift)
def create_shift(shift: WorkShift, session: Session = Depends(get_session)):
    """
    Record a shift
    """
    session.add(shift)
    session.commit()
    session.refresh(shift)
    return shift

@app.get("/shifts/", response_model=List[WorkShift])
def read_shifts(session: Session = Depends(get_session)):
    """
    Return list of shifts
    """
    shifts = session.exec(select(WorkShift)).all()
    return shifts

@app.post("/summary/{employee_id}/{year}/{month}")
def create_monthly_report(employee_id: int, year: int, month: int, monthly_bonus: Decimal = Decimal("0.00")):

    existing = get_existing_summary(employee_id, year, month)

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Report for that user {employee_id} for {month}/{year} already exists."
            )

    
    result = generate_monthly_summary(employee_id=employee_id, year=year, month=month, monthly_bonus=monthly_bonus)

    if result is None:
        return {
            "error": "There isn\'t active contract for this employee"
            }

    return result

@app.get("/summary/{employee_id}/{year}/{month}")
def read_monthly_report(employee_id: int, year: int, month: int):

    result = get_existing_summary(employee_id=employee_id, year=year, month=month)

    if result is None:
        return {"error": "Report for this month is not yet generated"}

    return result





