from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from database import Base
import datetime
from sqlalchemy.orm import relationship


class ModelUser(Base):
    __tablename__ = "user"
   
    id = Column(Integer, primary_key=True)
    username= Column(String(50), nullable=False)
    password= Column(String, nullable=False)
    user_type=Column(SmallInteger, nullable=False, default=1)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updatedAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
   
    user_information = relationship("ModelUserInformation", back_populates="user", uselist=False, cascade="all, delete-orphan")