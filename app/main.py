from dotenv import load_dotenv
load_dotenv()

from app.model.user.expense_category import ModelUserExpenseCategory
from app.model.user.user import ModelUser

from fastapi import FastAPI
from app.database import Base, engine
from app.route.user import user
from app.helper.system.expense_category import HelperSystemExpenseCategory
from app.helper.user.expense_category import HelperUserExpenseCategory

app = FastAPI()

Base.metadata.create_all(bind=engine)

HelperUserExpenseCategory.init_expense_category()
HelperSystemExpenseCategory.init_expense_category()

@app.get("/")
async def root():
    return 'OK'

app.include_router(user.router, prefix="/user", tags=["user"])