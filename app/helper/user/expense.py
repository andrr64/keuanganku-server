from sqlalchemy.orm import Session
from app.helper.response import HelperResponse
from app.model.user.expense import ModelUserExpense
class HelperExpense:
    @staticmethod
    def create_expense(db: Session, userid: int, categoryid: int, title: str, amount: float):
        new_expense= ModelUserExpense(userid=userid, categoryid=categoryid)
