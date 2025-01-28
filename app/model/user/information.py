from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
import datetime
from sqlalchemy.orm import relationship

class ModelUserInformation(Base):
    __tablename__ = "user_information"
  
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    name = Column(String(100), nullable=False, default="")
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updatedAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    
    user = relationship("ModelUser", back_populates="information", uselist=False)
