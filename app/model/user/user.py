import uuid
import datetime
from sqlalchemy import Column, String, DateTime, SmallInteger, UUID
from sqlalchemy.orm import relationship
from app.database import Base

class ModelUser(Base):
    __tablename__ = "user"
   
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_type = Column(SmallInteger, nullable=False, default=1)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updatedAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
   
    information = relationship("ModelUserInformation", back_populates="user", uselist=False, cascade="all, delete-orphan")
    expense_categories = relationship("ModelUserExpenseCategory", back_populates="user", cascade="all, delete-orphan")
    income_categories = relationship("ModelUserIncomeCategory", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("ModelUserExpense", back_populates="user", cascade="all, delete-orphan")
    incomes = relationship("ModelUserIncome", back_populates="user", cascade="all, delete-orphan")