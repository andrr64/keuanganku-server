from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.database import Base, engine
from app.route.user import user
from app.helper.system.expense_category import HelperSystemExpenseCategory
from app.helper.user.expense_category import HelperUserExpenseCategory
from app.helper.user.income_category import HelperUserIncomeCategory

app = FastAPI()

Base.metadata.create_all(bind=engine)

HelperUserExpenseCategory.init_expense_category()
HelperUserIncomeCategory.init_expense_category()
HelperSystemExpenseCategory.init_expense_category()

@app.get("/")
async def root():
    return 'KeuanganKu Server 0.0'

app.include_router(user.router, prefix="/user", tags=["user"])