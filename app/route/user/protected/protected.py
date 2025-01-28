from fastapi import APIRouter
from app.route.user.protected import update
from  app.route.user.protected import  expense_category
from app.route.user.protected import  income_category

router = APIRouter(
    prefix="/protected"
)

# router.include_router(router=expense_category.router)
# router.include_router(router=income_category.router)
router.include_router(router=update.router)