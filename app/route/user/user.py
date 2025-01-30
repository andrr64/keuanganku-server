from fastapi import APIRouter
from app.route.user import register, login, verify
from app.route.user.protected import protected


router = APIRouter()

router.include_router(register.router)      # user/register
router.include_router(login.router)         # user/login
router.include_router(verify.router)
router.include_router(protected.router)     # user/protected/...child (fitur-fitur yang perlu autentikasi)