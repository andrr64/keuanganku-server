from sqlalchemy.orm import Session
from app.model.system_expense_category import ModelSystemExpenseCategory
from app.database import engine, SessionLocal

class HelperSystemExpenseCategory:
    
    @staticmethod
    def init_expense_category():
        """ Memastikan tabel sudah ada dan menambahkan data jika tabel kosong """
        # Membuat tabel jika belum ada
        ModelSystemExpenseCategory.metadata.create_all(bind=engine)

        # Membuka sesi database untuk menambah data
        db: Session = SessionLocal()

        # Mengecek apakah sudah ada data dalam tabel
        existing_data = db.query(ModelSystemExpenseCategory).count()

        if existing_data == 0:
            # Menambahkan 5 data baru jika tabel kosong
            categories = [
                ModelSystemExpenseCategory(title="Food & Drink"),
                ModelSystemExpenseCategory(title="Transportation"),
                ModelSystemExpenseCategory(title="Entertainment"),
                ModelSystemExpenseCategory(title="Health"),
            ]
            
            db.add_all(categories)
            db.commit()
        
        db.close()

    @staticmethod
    def get_all_categories():
        """ Mengambil semua kategori dari tabel """
        db: Session = SessionLocal()
        categories = db.query(ModelSystemExpenseCategory).all()
        db.close()
        return categories

    @staticmethod
    def add_category(title: str):
        """ Menambahkan kategori baru """
        db: Session = SessionLocal()
        new_category = ModelSystemExpenseCategory(title=title)
        db.add(new_category)
        db.commit()
        db.close()
