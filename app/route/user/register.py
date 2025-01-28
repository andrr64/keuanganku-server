from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controller.user.user import ControllerUser
from pydantic import BaseModel
from app.database import get_db

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
    if not controller_response.success:
        raise HTTPException(
            status_code=controller_response.http_code,
            detail=controller_response.message
        )
    return controller_response.to_dict()