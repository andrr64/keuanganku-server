from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        print("Berhasil terhubung dengan database")
except Exception as e:
    print("Gagal terhubung dengan database") 
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()