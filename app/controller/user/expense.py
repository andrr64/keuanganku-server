from sqlalchemy.orm import Session
from app.helper.user.user import HelperUser
from app.controller.response import ControllerResponse
from app.model.user.user import ModelUser
from app.model.user.expense import ModelUserExpense

class ControllerUserExpense:
    @staticmethod
    def add_expense(db: Session, title: str, amount: float, username: str, category_id: int):
        find_user = HelperUser.read_user_by_username(db=db, username=username)
        if not find_user.success:
            return ControllerResponse.not_found(err_message="Invalid user")
        user: ModelUser= find_user.data
        category = next(
            (category for category in user.expense_categories if category.id == category_id),
            None
        )
        if category is None:
            return ControllerResponse.not_found(err_message="Category not found")
        new_expense = ModelUserExpense(title=title, amount=amount, category_id=category_id)