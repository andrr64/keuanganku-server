from fastapi import APIRouter, Depends, Response, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user.user import ControllerUser
from app.controller.response import handle_controller_response
from app.logger import log

router = APIRouter()

class LoginFields(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login_user(user: LoginFields, response: Response, request: Request, db: Session = Depends(get_db)):
    # Mendapatkan header Origin dari request
    origin = request.headers.get('Origin', 'No Origin header')
    
    # Menampilkan origin di log
    log.info(f"ORIGIN: {origin}")
    
    controller_response = ControllerUser.login_user(
        db=db,
        username=user.username,
        password=user.password,
        response=response
    )
    
    return handle_controller_response(controller_response)
