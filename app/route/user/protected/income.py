from typing import Any
from fastapi import  status, HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import  Session
from app.database import get_db
from app.middleware.token import validate_token
from pydantic import BaseModel, field_validator
from app.controller.response import handle_controller_response
from app.controller.user.income import ControllerUserIncome

# FIELDS
class AddIncomeFields(BaseModel):
    title: str
    category_id: str
    amount: float

    @field_validator('title')
    def validate_title(cls, value: any):
        if len(value) <= 0 or len(value) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title can't empty and max chars is 50"
            )
        return value
    
    @field_validator('amount')
    def validate_amount(cls, value: Any):
        if value <= 0 or value > 1_000_000_000_000_000:
            raise  HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Min=0 and Max=1,000,000,000,000,000"
            )
        return value

# ROUTER & ROUTE
router = APIRouter()

@router.get(path='/')
async def get_income(user_id: str = Depends(validate_token), db= Depends(get_db)):
    return handle_controller_response(
        ctrl_res=ControllerUserIncome.get_income(db=db, user_id=user_id)
    )
    
@router.post(path='/')
async def add_income(body: AddIncomeFields, user_id: str= Depends(validate_token), db: Session= Depends(get_db)):
    category_id = body.category_id
    title = body.title
    amount = body.amount
    return handle_controller_response(
        ctrl_res=ControllerUserIncome.add_income(db=db, user_id=user_id, category_id=category_id, title=title, amount=amount)
    )