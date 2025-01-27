from dotenv import load_dotenv
load_dotenv("../.env")

from fastapi import FastAPI
from app.database import Base, engine
from app.route import user
from app.helper.system_expense_category import HelperSystemExpenseCategory

app = FastAPI()

Base.metadata.create_all(bind=engine)
HelperSystemExpenseCategory.init_expense_category()

@app.get("/")
async def root():
    return 'OK'

app.include_router(user.router, prefix="/user", tags=["user"])