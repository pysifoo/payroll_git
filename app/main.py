from fastapi import FastAPI, HTTPException
from decimal import Decimal

from sqlmodel import select, Session
from app.monthly_summary import generate_monthly_summary, get_existing_summary


app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Working API payroll calculator."} 


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


