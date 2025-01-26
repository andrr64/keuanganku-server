from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class ModelAccount(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    username= Column(String(50), nullable=False)
    password= Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    