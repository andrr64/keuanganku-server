from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

# Menggunakan string untuk mendefinisikan relasi dengan ModelUserExpenseCategory
class ModelUser(Base):
    __tablename__ = "user"
   
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(SmallInteger, nullable=False, default=1)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updatedAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
   
    user_information = relationship("ModelUserInformation", back_populates="user", uselist=False, cascade="all, delete-orphan")
    expense_categories = relationship("ModelUserExpenseCategory", back_populates="user", cascade="all, delete-orphan")
