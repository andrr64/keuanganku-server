from sqlalchemy.orm import Session
from app.controller.response import ControllerResponse
from app.model.user.expense_category import ModelUserExpenseCategory
from app.helper.user.expense import HelperExpense
from app.model.user import expense

class ControllerUserExpense:
    
    @staticmethod
    def get_expense(db: Session, user_id: str):
        helper_response = HelperExpense.get_expense_by_userid(db=db, user_id=user_id)
        if not helper_response.success:
            return ControllerResponse.error(err_message=helper_response.message)
        return ControllerResponse.success(data=[
            expense.filter_data(x) for x in helper_response.data
        ])

    @staticmethod
    def add_expense(db: Session, user_id: str, category_id: str, title: str, amount: float) -> ControllerResponse:
        category_exists = db.query(ModelUserExpenseCategory).filter(
            ModelUserExpenseCategory.userid == user_id,
            ModelUserExpenseCategory.id == category_id
        ).first()
        if not category_exists:
            return ControllerResponse.not_found(err_message="User or category not found, please re-login or refresh.")
        
        helper_response = HelperExpense.create_expense(db, user_id, category_id, title, amount)
        if not helper_response.success:
            return ControllerResponse.error(err_message="Something wrong when save data")
        return ControllerResponse.success(data=expense.filter_data(helper_response.data))