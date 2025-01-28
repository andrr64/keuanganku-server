from fastapi import APIRouter, Depends
from app.middleware.validate_token import validate_token
from app.route.user.protected.add import add
from app.route.user.protected import update

router = APIRouter(
    prefix="/protected"
)

router.include_router(router=add.router, prefix="/add")
router.include_router(router=update.router)