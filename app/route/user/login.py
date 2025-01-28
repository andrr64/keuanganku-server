from fastapi import APIRouter, HTTPException, Depends, Response, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user.user import ControllerUser
from os import getenv


debug = getenv("debug") == 'yes'
router = APIRouter()

class FormLoginUser(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login_user(user: FormLoginUser, db: Session = Depends(get_db), response: Response= None):
    response_data = ControllerUser.login_user(db=db, username=user.username, password=user.password)
    if (response_data.success):
        token = response_data.data["access_token"]
        response.set_cookie(
            key="access_token", # Nama cookie
            value=token,        # Nilai token JWT
            httponly=True,      # Menghindari akses dari JavaScript
            secure=not debug,        # Hanya untuk koneksi HTTPS
            samesite="Strict",  # Menghindari CSRF
            max_age=ControllerUser.access_token_expired,  # Set waktu kadaluarsa cookie (misal 1 jam)
        )
        return response_data.to_dict()
    raise HTTPException(
        status_code=response_data.http_code,
        detail=response_data.message
    )
