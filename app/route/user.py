from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from model.user import ModelUser
from helper.response import HelperResponse
from controller.user import ControllerUser
from controller.response import ControllerResponse

router = APIRouter()

class RegisterUser(BaseModel):
    username: str
    password: str

# Endpoint untuk register
@router.post("/register")
async def register_user(user: RegisterUser, db: Session = Depends(get_db)):
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
        
# Endpoint untuk login
@router.post("/login")
async def login_user(user: RegisterUser, db: Session = Depends(get_db), response: Response= None):
    response_data = ControllerUser.login_user(db=db, username=user.username, password=user.password)
    if (response_data.success):
        token = response_data.data["access_token"]
                # Set cookie untuk token
        response.set_cookie(
            key="access_token",  # Nama cookie
            value=token,  # Nilai token JWT
            httponly=True,  # Menghindari akses dari JavaScript
            secure=True,  # Hanya untuk koneksi HTTPS
            samesite="Strict",  # Menghindari CSRF
            max_age=ControllerUser.access_token_expired,  # Set waktu kadaluarsa cookie (misal 1 jam)
        )
        
        return response_data.to_dict()
    raise HTTPException(
        status_code=response.http_status_code,
        detail=response.message
    )
