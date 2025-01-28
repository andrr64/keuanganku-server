from sqlalchemy.orm import Session
from app.model.user.user import ModelUser
from app.controller.user.user import  ControllerResponse
from app.helper.user.income_category import HelperUserIncomeCategory
from fastapi import status, HTTPException

class ControllerUserIncomeCategory:
    @staticmethod
    def add_income_category(db: Session, user:ModelUser, title: str) -> ControllerResponse:
        if HelperUserIncomeCategory.is_like_category_exists(db=db, user=user, title=title):
            return ControllerResponse.error(
                err_message='Category already exists',
                http_code=status.HTTP_409_CONFLICT
            )
        response = HelperUserIncomeCategory.create_expense_category(db=db, user=user, title=title)
        if not response.success:
            return ControllerResponse.error(err_message=response.message)
        return ControllerResponse.success(data=response.data)