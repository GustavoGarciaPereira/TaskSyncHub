import os

from fastapi import Header, HTTPException, status
from dotenv import load_dotenv

# Token estático para simplificar a autenticação
load_dotenv()

STATIC_API_TOKEN = os.getenv('STATIC_API_TOKEN')

async def verify_token(token: str = Header(...)):
    """
    Verifica se o token enviado no header 'token' é válido.
    Se não for, lança uma exceção HTTP 401.
    """
    if token != STATIC_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token"
        )