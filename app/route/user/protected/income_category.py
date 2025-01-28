from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.token import validate_token
from app.controller.response import handle_controller_response
from app.controller.user.income_category import ControllerUserIncomeCategory

class AddIncomeCategoryFields(BaseModel):
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

@router.post(path='/')
async def add_income_category(
    body: AddIncomeCategoryFields,
    db: Session= Depends(get_db),
    user_id: str = Depends(validate_token)
):
    return handle_controller_response(
        ControllerUserIncomeCategory.add_income_category(db=db, user_id=user_id, title=body.title)
    ) 

@router.get(path='/')
async def get_income_category(
    db: Session= Depends(get_db),
    user_id: str = Depends(validate_token)
): 
    return handle_controller_response(
        ControllerUserIncomeCategory.get_income_category(
            db=db,
            user_id=user_id
        )
    )