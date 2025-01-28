from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user.user import ControllerUser
from app.controller.response import handle_controller_response

router = APIRouter()

class LoginFields(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login_user(user: LoginFields, response: Response, db: Session = Depends(get_db)):
    controller_response = ControllerUser.login_user(
        db=db,
        username=user.username,
        password=user.password,
        response=response
    )
    return handle_controller_response(controller_response)