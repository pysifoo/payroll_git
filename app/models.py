from typing import Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal
from datetime import date, datetime

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    has_tax_relief: bool = True


class Contract(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    contract_type: str
    hourly_rate: Decimal = Field(max_digits=10,
                                 decimal_places=2)


class WorkShift(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    start_time: datetime
    end_time: datetime

class MonthlyWorkRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    year: int
    month: int
    regular_hours: Decimal = Field(max_digits=10,
                                   decimal_places=2)
    night_hours: Decimal = Field(max_digits=10,
                                   decimal_places=2)
    monthly_bonus: Decimal = Field(default=Decimal("0"), max_digits=10, decimal_places=2)
    overtime_50_hours: Decimal = Field(max_digits=10, decimal_places=2)
    overtime_100_hours: Decimal = Field(max_digits=10, decimal_places=2)
    total_gross: Decimal = Field(max_digits=10, decimal_places=2)
    total_net: Decimal = Field(max_digits=10, decimal_places=2)
