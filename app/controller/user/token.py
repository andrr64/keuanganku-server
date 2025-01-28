from fastapi import Response
from os import getenv
from datetime import timedelta

debug= getenv('debug') == 'yes'
access_token_expired = timedelta(hours=24)

def set_access_token(token: str, response: Response):
    response.set_cookie(
        key="access_token", # Nama cookie
        value=token,        # Nilai token JWT
        httponly=True,      # Menghindari akses dari JavaScript
        secure=not debug,        # Hanya untuk koneksi HTTPS
        samesite="Strict",  # Menghindari CSRF
        max_age=access_token_expired,  # Set waktu kadaluarsa cookie (misal 1 jam)
    )