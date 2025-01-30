from fastapi import APIRouter, Depends, Response, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user.user import ControllerUser
from app.controller.response import handle_controller_response
from app.middleware.token import validate_token
from app.logger import log

router = APIRouter()

@router.get("/verify-token")
async def user_verify(username: str= Depends(validate_token)):
    return {
        "detail": "OK",
        "status": True,
        "data": None
    }