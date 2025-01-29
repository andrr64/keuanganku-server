from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.user.user import ControllerUser
from pydantic import BaseModel, field_validator
from app.database import get_db
from app.controller.response import handle_controller_response
from fastapi import HTTPException, status

# FIELDS
class RegisterFields(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, val):
        if len (val) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The password must contain a minimum of 8 characters"
            )
        return val
    
# ROUTER & ROUTE
router = APIRouter()

@router.post("/register")
async def register_user(body: RegisterFields, db: Session = Depends(get_db)):
    controller_response = ControllerUser.create_user(
        db=db, 
        username=body.username,
        password=body.password
    )
    return handle_controller_response(controller_response)