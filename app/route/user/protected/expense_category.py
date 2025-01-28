from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user.expense_category import ControllerUserExpenseCategory
from app.middleware.token import validate_token
from app.controller.response import handle_controller_response

class AddExpenseCategoryFields(BaseModel):
    title: str
    @field_validator('title')
    def validate_title(cls, v):
        v_len = len(v)
        if v_len >= 50:
            raise HTTPException(
                status_code=400,
                detail="Maximum title chars is 50"
            )
        elif v_len <= 0:
            raise HTTPException(
                status_code=400,
                detail="Title can't be empty, Bro."
            )
        return v

router = APIRouter()

@router.post('/')
async def add_expense_category(
    body: AddExpenseCategoryFields, 
    db: Session= Depends(get_db), 
    user_id: str = Depends(validate_token)
):
    controller_response = ControllerUserExpenseCategory.add_expense_category(db=db, user_id=user_id, title=body.title)
    return handle_controller_response(controller_response)

@router.get(path='/')
async def get_expense_category(
    db: Session = Depends(get_db),
    user_id: str= Depends(validate_token)
):
    controller_response = ControllerUserExpenseCategory.get_expense_category(db=db, user_id=user_id)
    return handle_controller_response(controller_response)