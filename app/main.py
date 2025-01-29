from app.model.user.income import ModelUserIncome
from app.model.user.expense import ModelUserExpense

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.route.user import user
from app.helper.user.expense_category import HelperUserExpenseCategory
from app.helper.user.income_category import HelperUserIncomeCategory
from app.route import check_token

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Menambahkan CORS Middleware dengan format yang benar
origins = [
    "http://localhost:5173",
    "http://192.168.1.8:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Menetapkan origins yang diizinkan
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode HTTP (GET, POST, PUT, DELETE, dll)
    allow_headers=["*"],  # Mengizinkan semua header
)

HelperUserExpenseCategory.init_expense_category()
HelperUserIncomeCategory.init_expense_category()

@app.get("/")
async def root():
    return 'KeuanganKu Server 0.0'

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(check_token.router)