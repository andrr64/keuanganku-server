from fastapi import FastAPI
from database import Base, engine
from route import user


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/user", tags=["user"])