from typing import Protocol, Self
from jose import jwt
from datetime import datetime, UTC, timedelta
from settings import settings

class InternalTokenServiceProtocol(Protocol):
    async def generate_internal_token(self: Self) -> str:
        ...

class InternalTokenService(InternalTokenServiceProtocol):
    async def generate_internal_token(self: Self) -> str:
        MINUTES_TIME = settings.email_service.token_lifetime_minutes
        ALGORITHM = settings.email_service.token_algorithm
        SECRET_KEY = settings.email_service.secret_key
        payload = {
            "iss": "main-service", 
            "permissions": ["send:email"],
            "exp": datetime.now(UTC) + timedelta(minutes=MINUTES_TIME)
        }
        
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )