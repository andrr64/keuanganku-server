from sqlalchemy.orm import Session
from app.helper.response import HelperResponse
from app.model.user.expense import ModelUserExpense
from app.logger import log

class HelperExpense:
    @staticmethod
    def create_expense(db: Session, userid: str, categoryid: str, title: str, amount: float):
        new_expense = ModelUserExpense(userid=userid, categoryid=categoryid, title=title, amount=amount)
        try:
            db.add(new_expense)
            db.commit()
            return HelperResponse.success(data=new_expense)
        except Exception as e:
            db.rollback()
            log.error(str(e))
            return HelperResponse.error(err_message=f'an error occurred: {str(e)}')

    @staticmethod
    def get_expense_by_userid(db: Session, user_id: str):  # change expense_id to str
        try:
            result= db.query(ModelUserExpense).filter(
                ModelUserExpense.userid == user_id
            ).all()
            return HelperResponse.success(data=result)
        except Exception as e:
            log.error(str(e))
            return HelperResponse.error(err_message=f'an error occurred: {str(e)}')

    @staticmethod
    def update_expense(db: Session, expense_id: str, userid: str = None, categoryid: str = None, title: str = None, amount: float = None):
        try:
            expense = db.query(ModelUserExpense).filter(ModelUserExpense.id == expense_id).first()  # Use expense_id as str
            if not expense:
                return HelperResponse.error(err_message='Expense not found', status_code=404)

            if userid:
                expense.userid = userid
            if categoryid:
                expense.categoryid = categoryid
            if title:
                expense.title = title
            if amount:
                expense.amount = amount

            db.commit()
            return HelperResponse.success(data=expense)
        except Exception as e:
            db.rollback()
            log.error(str(e))
            return HelperResponse.error(err_message=f'an error occurred: {str(e)}')

    @staticmethod
    def delete_expense(db: Session, expense_id: str):  # change expense_id to str
        try:
            expense = db.query(ModelUserExpense).filter(ModelUserExpense.id == expense_id).first()  # Use expense_id as str
            if not expense:
                return HelperResponse.error(err_message='Expense not found', status_code=404)

            db.delete(expense)
            db.commit()
            return HelperResponse.success(message='Expense deleted successfully')
        except Exception as e:
            db.rollback()
            log.error(str(e))
            return HelperResponse.error(err_message=f'an error occurred: {str(e)}')
