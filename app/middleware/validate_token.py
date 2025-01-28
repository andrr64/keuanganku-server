from fastapi import HTTPException, status, Request, Response
import jwt
import os

SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
ALGORITHM = os.getenv("TOKEN_ALGORITHM")

def delete_access_token(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="Strict",
    )


def validate_token(request: Request, response: Response) -> str:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            delete_access_token(response)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return username
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