from fastapi import APIRouter, HTTPException, Depends, Response, Request
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user.user import ControllerUser
from app.controller.user.add.expense_category import ControllerUserExpenseCategory
from app.helper.user.user import HelperUser
from app.middleware.validate_token import validate_token

class Field(BaseModel):
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

@router.post('/expense-category')
async def add_expense_category(
    body: Field, 
    db: Session= Depends(get_db), 
    username: str = Depends(validate_token)
):
    user = HelperUser.read_user_by_username(db=db, username=username).data
    controllerResponse = ControllerUserExpenseCategory.add_expense_category(db=db, user=user, title=body.title)
    if (not controllerResponse.success):
        raise HTTPException(
            status_code=controllerResponse.http_code,
            detail=controllerResponse.message
        )
    return controllerResponse.to_dict()