from sqlalchemy.orm import Session
from app.model.user.user import ModelUser
from app.controller.user.user import  ControllerResponse
from app.helper.user.expense_category import HelperUserExpenseCategory
from fastapi import status, HTTPException

class ControllerUserExpenseCategory:
    @staticmethod
    def add_expense_category(db: Session, user:ModelUser, title: str) -> ControllerResponse:
        
        if (HelperUserExpenseCategory.is_like_category_exists(db=db, user=user, title=title)):
            return ControllerResponse.error(
                err_message='Category already exists',
                http_code=status.HTTP_409_CONFLICT
            )
        
        response = HelperUserExpenseCategory.create_expense_category(db=db, user=user, title=title)
        print(response.message)
        if (not response.success):
            return ControllerResponse.error(err_message=response.message)
        return ControllerResponse.success(data=response.data)