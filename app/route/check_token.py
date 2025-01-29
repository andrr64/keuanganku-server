from fastapi import APIRouter, Request

router = APIRouter()


@router.post('/check-token')
def check_token(request: Request):
    access_token = request.cookies.get("access_token")
    return access_token