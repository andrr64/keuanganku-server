from fastapi import APIRouter, Depends
from app.middleware.validate_token import validate_token
from app.route.user.auth.add import add
from app.route.user.auth import update

router = APIRouter(
    prefix="/auth",
    dependencies=[Depends(validate_token)]
)

router.include_router(router=add.router, prefix="/add")
router.include_router(router=update.router)