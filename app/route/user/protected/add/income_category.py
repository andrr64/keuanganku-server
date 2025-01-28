from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user.add.income_category import ControllerUserIncomeCategory
from app.helper.user.user import HelperUser
from app.middleware.validate_token import validate_token

class RequestFields(BaseModel):
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

@router.post('/income-category')
async def add_income_category(
    body: RequestFields,
    db: Session= Depends(get_db), 
    username: str = Depends(validate_token)
):
    user = HelperUser.read_user_by_username(
        db=db,
        username=username).data
    controller_response = ControllerUserIncomeCategory.add_income_category(
        db=db,
        user=user,
        title=body.title
    )
    if not controller_response.success:
        raise HTTPException(
            status_code=controller_response.http_code,
            detail=controller_response.message
        )
    return controller_response.to_dict()