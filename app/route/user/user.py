from fastapi import APIRouter
from app.route.user import register
from app.route.user import login
from app.route.user.auth import auth

router = APIRouter()

router.include_router(register.router) # /register
router.include_router(login.router) # /login
router.include_router(auth.router) # /auth/...child