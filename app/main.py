from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.database import Base, engine
from app.route import user


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return 'OK'

app.include_router(user.router, prefix="/user", tags=["user"])