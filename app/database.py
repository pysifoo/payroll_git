import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from app.models import Employee, Contract, WorkShift, MonthlyWorkRecord

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{postgres_db}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()

