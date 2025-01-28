from fastapi import HTTPException, status, Request, Response
import jwt
from os import  getenv
from datetime import  timedelta
import uuid

SECRET_KEY = getenv("TOKEN_SECRET_KEY")
ALGORITHM = getenv("TOKEN_ALGORITHM")
debug= getenv('debug') == 'yes'
access_token_expired = timedelta(hours=24)

def delete_access_token(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="strict",
    )

def validate_token(request: Request, response: Response) -> uuid:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )
    try:
        # Decode token and validate
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")  # Menggunakan 'id' sebagai payload key
        if user_id is None:
            delete_access_token(response)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return user_id
    except jwt.ExpiredSignatureError:
        delete_access_token(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        delete_access_token(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
def create_access_token(id: any) -> str:
    data = {"id": str(id)}
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def set_access_token(token: str, response: Response):
    response.set_cookie(
        key="access_token",             # Nama cookie
        value=token,                    # Nilai token JWT
        httponly=True,                  # Menghindari akses dari JavaScript
        secure=not debug,               # Hanya untuk koneksi HTTPS
        samesite="strict",              # Menghindari CSRF
        max_age=access_token_expired,   # Set waktu kadaluarsa cookie (misal 1 jam)
    )