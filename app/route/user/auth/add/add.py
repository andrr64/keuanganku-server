from fastapi import APIRouter

router = APIRouter()

from app.route.user.auth.add import expense_category
router.include_router(expense_category.router)