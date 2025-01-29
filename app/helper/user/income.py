from sqlalchemy.orm import Session
from app.helper.response import HelperResponse
from app.model.user.income import ModelUserIncome
from app.logger import log

class HelperIncome:
    @staticmethod
    def create_income(db: Session, userid: str, categoryid: str, title: str, amount: float):
        new_income = ModelUserIncome(userid=userid, categoryid=categoryid, title=title, amount=amount)
        try:
            db.add(new_income)
            db.commit()
            return HelperResponse.success(data=new_income)
        except Exception as e:
            db.rollback()
            log.error(str(e))
            return HelperResponse.error(err_message=f'an error occurred: {str(e)}')

    @staticmethod
    def get_income_by_userid(db: Session, user_id: str):
        try:
            result = db.query(ModelUserIncome).filter(
                ModelUserIncome.userid == user_id
            ).all()
            return HelperResponse.success(data=result)
        except Exception as e:
            log.error(str(e))
            return HelperResponse.error(err_message=f'an error occurred: {str(e)}')

    @staticmethod
    def update_income(db: Session, income_id: str, userid: str = None, categoryid: str = None, title: str = None, amount: float = None):
        try:
            income = db.query(ModelUserIncome).filter(ModelUserIncome.id == income_id).first()
            if not income:
                return HelperResponse.error(err_message='Income not found', status_code=404)

            if userid:
                income.userid = userid
            if categoryid:
                income.categoryid = categoryid
            if title:
                income.title = title
            if amount:
                income.amount = amount

            db.commit()
            return HelperResponse.success(data=income)
        except Exception as e:
            db.rollback()
            log.error(str(e))
            return HelperResponse.error(err_message=f'an error occurred: {str(e)}')

    @staticmethod
    def delete_income(db: Session, income_id: str):
        try:
            income = db.query(ModelUserIncome).filter(ModelUserIncome.id == income_id).first()
            if not income:
                return HelperResponse.error(err_message='Income not found', status_code=404)

            db.delete(income)
            db.commit()
            return HelperResponse.success(message='Income deleted successfully')
        except Exception as e:
            db.rollback()
            log.error(str(e))
            return HelperResponse.error(err_message=f'an error occurred: {str(e)}')
