from fastapi import APIRouter
from app.route.user.protected.add import expense_category, income_category


router = APIRouter()

router.include_router(expense_category.router)
router.include_router(income_category.router)
