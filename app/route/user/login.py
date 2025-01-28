from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user.user import ControllerUser

router = APIRouter()

class RequestFields(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login_user(user: RequestFields, db: Session = Depends(get_db), response: Response= None):
    controller_response = ControllerUser.login_user(
        db=db,
        username=user.username,
        password=user.password,
        response=response
    )
    if not controller_response.success:
        raise HTTPException(
            status_code=controller_response.http_code,
            detail=controller_response.message
        )
    return controller_response.to_dict()