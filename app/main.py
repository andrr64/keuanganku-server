from app.model.user.income import ModelUserIncome
from app.model.user.expense import ModelUserExpense

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.database import Base, engine
from app.route.user import user
from app.helper.user.expense_category import HelperUserExpenseCategory
from app.helper.user.income_category import HelperUserIncomeCategory
from app.route import check_token

app = FastAPI()

Base.metadata.create_all(bind=engine)

HelperUserExpenseCategory.init_expense_category()
HelperUserIncomeCategory.init_expense_category()

@app.get("/")
async def root():
    return 'KeuanganKu Server 0.0'

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(check_token.router)