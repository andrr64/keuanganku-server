from fastapi import APIRouter, Request, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.controller.user.user import ControllerUser
from pydantic import BaseModel

from app.database import get_db
from app.middleware.validate_token import validate_token
from app.controller.user.token import set_access_token

router = APIRouter()

class FormUpdateUser(BaseModel):
    new_username: str | None = None
    new_password: str | None = None
    name: str
    
@router.put('/update')
async def update_userinfo(
    form: FormUpdateUser, 
    db: Session= Depends(get_db), 
    username:str= Depends(validate_token),
    response: Response= None
):
    controller_response = ControllerUser.update_userinfo(
        db=db,
        oldUsername=username,
        new_username=form.new_username,
        new_password=form.new_password,
        response= response,
        name=form.name 
    )
    if not controller_response.success:
        raise HTTPException(
            status_code=controller_response.http_code,
            detail=controller_response.message
        )
    return controller_response.to_dict()