from sqlalchemy.orm import Session
from app.model.user.user import ModelUser
from app.controller.user.user import  ControllerResponse
from app.helper.user.expense_category import HelperUserExpenseCategory
from fastapi import status
from app.helper.user.user import HelperUser

class ControllerUserExpenseCategory:
    @staticmethod
    def add_expense_category(db: Session, user:ModelUser, title: str) -> ControllerResponse:
        if HelperUserExpenseCategory.is_like_category_exists(db=db, user=user, title=title):
            return ControllerResponse.error(
                err_message='Category already exists',
                http_code=status.HTTP_409_CONFLICT
            )
        response = HelperUserExpenseCategory.create_expense_category(db=db, user=user, title=title)
        print(response.message)
        if not response.success:
            return ControllerResponse.error(err_message=response.message)
        return ControllerResponse.success(data=response.data)

    @staticmethod
    def get_expense_category(db: Session, username: str) -> ControllerResponse:
        find_user = HelperUser.read_user_by_username(db=db, username=username)
        if not find_user.success:
            return ControllerResponse.error(err_message=find_user.message)
        user: ModelUser = find_user.data
        return ControllerResponse.success(
            data=user.expense_categories
        )