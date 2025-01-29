from sqlalchemy.orm import Session
from app.controller.response import ControllerResponse
from app.model.user.income_category import ModelUserIncomeCategory
from app.helper.user.income import HelperIncome
from app.model.user import income

class ControllerUserIncome:
    
    @staticmethod
    def get_income(db: Session, user_id: str):
        helper_response = HelperIncome.get_income_by_userid(db=db, user_id=user_id)
        if not helper_response.success:
            return ControllerResponse.error(err_message=helper_response.message)
        return ControllerResponse.success(data=[
            income.filter_data(x) for x in helper_response.data
        ])

    @staticmethod
    def add_income(db: Session, user_id: str, category_id: str, title: str, amount: float) -> ControllerResponse:
        category_exists = db.query(ModelUserIncomeCategory).filter(
            ModelUserIncomeCategory.userid == user_id,
            ModelUserIncomeCategory.id == category_id
        ).first()
        if not category_exists:
            return ControllerResponse.not_found(err_message="User or category not found, please re-login or refresh.")
        
        helper_response = HelperIncome.create_income(db, user_id, category_id, title, amount)
        if not helper_response.success:
            return ControllerResponse.error(err_message="Something wrong when saving data")
        return ControllerResponse.success(data=income.filter_data(helper_response.data))
