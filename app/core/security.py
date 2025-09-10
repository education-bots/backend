from fastapi import HTTPException, Header

from app.config import settings


async def verify_auth_header(x_api_client: str = Header(..., alias=settings.frontend_auth_header)) -> str:
    """Verify the authentication header"""
    if x_api_client != settings.frontend_auth_secret:
        raise HTTPException(
            status_code=401,
            detail="Invalid API client authentication"
        )
    return x_api_client

