from app.model.user.expense_category import ModelUserExpenseCategory
from app.database import engine


class HelperUserExpenseCategory:
    @staticmethod
    def init_expense_category():
        """ Memastikan tabel sudah ada dan menambahkan data jika tabel kosong """
        ModelUserExpenseCategory.metadata.create_all(bind=engine)