from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.user.user import ControllerUser
from pydantic import BaseModel
from app.database import get_db
from app.controller.response import handle_controller_response

class RequestFields(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/register")
async def register_user(body: RequestFields, db: Session = Depends(get_db)):
    controller_response = ControllerUser.create_user(
        db=db, 
        username=body.username,
        password=body.password
    )
    return handle_controller_response(controller_response)