from fastapi import APIRouter, Request, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.controller.user.user import ControllerUser
from starlette import status as HTTPStatus
from pydantic import BaseModel
from app.controller.response import ControllerResponse
from app.database import get_db

class FormRegisterUser(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/register")
async def register_user(user: FormRegisterUser, db: Session = Depends(get_db)):
    response: ControllerResponse = ControllerUser.create_user(
        db=db, 
        username=user.username, 
        password=user.password
    )
    
    if response.success:
        return {"message": response.message}
    else:
        raise HTTPException(
            status_code=response.http_code,  # Gunakan status code dari HelperResponse
            detail=response.message  # Gunakan pesan dari HelperResponse
        )