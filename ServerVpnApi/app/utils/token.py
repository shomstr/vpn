from fastapi import HTTPException, Query
from starlette import status

from app.settings import settings


async def validate_connection_token(
    # FastAPI автоматически извлечет connection_token из query-параметров.
    # '...' означает, что параметр обязательный.
    # description будет отображено в документации (Swagger UI/ReDoc).
    connection_token: str = Query(..., description="Authentication token (required) for accessing this API.")
):
    """
    Зависимость, которая проверяет токен 'connection_token' из query-параметров.
    Если токен не предоставлен или невалиден, выбрасывает HTTPException 401.
    """
    if connection_token != settings.connection_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token."
        )
    # Если токен валиден, его можно вернуть.
    # Тогда эндпоинт, который использует эту зависимость, получит значение токена.
    return connection_token