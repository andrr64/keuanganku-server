from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.controller.user.user import ControllerUser
from pydantic import BaseModel
from app.database import get_db
from app.middleware.token import validate_token
import uuid
from app.controller.response import handle_controller_response


# FIELDS
class FormUpdateUser(BaseModel):
    new_username: str | None = None
    new_password: str | None = None
    new_name: str | None = None

# ROUTER & ROUTE
router = APIRouter()

@router.put('/update')
async def update_userinfo(
    form: FormUpdateUser, 
    db: Session= Depends(get_db), 
    user_id:uuid = Depends(validate_token),
    response: Response= None
):
    controller_response = ControllerUser.update_user(
        db=db,
        user_id=user_id,
        response=response,
        new_name=form.new_name,
        new_password=form.new_password,
        new_username=form.new_username
    )
    return handle_controller_response(controller_response)