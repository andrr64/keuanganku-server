# from typing import Any
# from fastapi import  status, HTTPException

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import  Session
# from app.database import get_db
# from app.middleware.validate_token import validate_token
# from pydantic import BaseModel, field_validator

# router = APIRouter()

# @router.get(path='/get/expense')
# async def get_expense():
#     pass

# class AddExpenseFields(BaseModel):
#     title: str
#     category_id: int
#     amount: float

#     @field_validator('amount')
#     def validate_amount(cls, value: Any):
#         if value <= 0 or value > 1_000_000_000_000:
#             raise  HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Min=0 and Max=1,000,000,000,000"
#             )
#         return value

# @router.post(path='/add/expense')
# async def add_expense(username: str= Depends(), db: Session= Depends(get_db)):

#     pass