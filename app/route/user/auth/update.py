from fastapi import APIRouter, Request, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.controller.user.user import ControllerUser
from starlette import status as HTTPStatus
from pydantic import BaseModel

from app.database import get_db

router = APIRouter()

class FormUpdateUser(BaseModel):
    username: str
    new_username: str | None = None
    new_password: str | None = None
    name: str
    
@router.put('/update')
async def update_userinfo(request: Request, form: FormUpdateUser, db: Session= Depends(get_db), response: Response = None):
    access_token = request.cookies.get("access_token")
    controllerResponse = ControllerUser.update_userinfo(
        db=db,
        token=access_token,
        oldUsername=form.username,
        new_username=form.new_username,
        new_password=form.new_password,
        name=form.name 
    )
    if controllerResponse.http_code == HTTPStatus.HTTP_401_UNAUTHORIZED:
        response.delete_cookie(
            key="access_token",  # Nama cookie yang ingin dihapus
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        raise HTTPException(
            status_code=HTTPStatus.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    elif not controllerResponse.success:
        raise HTTPException(
            status_code=controllerResponse.http_code,
            detail=controllerResponse.message
        )
    return controllerResponse.to_dict()