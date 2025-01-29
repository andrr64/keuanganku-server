from fastapi import APIRouter
from app.route.user.protected import update, expense_category, income_category, expense, income

router = APIRouter(
    prefix="/protected"
)

router.include_router(router=expense_category.router, prefix="/expense-category")
router.include_router(router=income_category.router, prefix="/income-category")
router.include_router(router=expense.router, prefix="/expense")
router.include_router(router=income.router, prefix="/income")
router.include_router(router=update.router)