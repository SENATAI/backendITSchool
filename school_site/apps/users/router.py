from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from .schemas import LoginRequestSchema, UserReadSchema
from .use_cases.login import LoginUseCaseProtocol
from .use_cases.refresh import RefreshUseCaseProtocol
from .depends import get_refresh_use_case
from .depends import get_login_use_case
from school_site.settings import settings


router = APIRouter(prefix='/api/users', tags=['Users'])

@router.post("/auth", response_model=UserReadSchema)
async def login(
    response: Response,
    user_data: LoginRequestSchema,
    login_use_case: LoginUseCaseProtocol = Depends(get_login_use_case)
):
    user_tokens_data = await login_use_case(
        user_data.username, user_data.password
    )
    
    response.set_cookie(
        key="access_token",
        value=user_tokens_data.access_token.token,
        httponly=True,
        secure=False,  # TODO: В продакшн с HTTPS
        samesite="lax",
        expires=settings.access_token.token_lifetime_minutes * 60,
        path="/"
    )
    
    response.set_cookie(
        key="refresh_token",
        value=user_tokens_data.refresh_token.token,
        httponly=True,
        secure=False,  # TODO: В продакшн с HTTPS
        samesite="lax",
        expires=settings.refresh_token.token_lifetime_days * 24 * 60 * 60,
        path="/"
    )
    
    return user_tokens_data.user

@router.post("/refresh", response_model=UserReadSchema)
async def refresh_token(
    response: Response,
    refresh_use_case: RefreshUseCaseProtocol = Depends(get_refresh_use_case),
    refresh_token: str = Cookie(...)
):
    user_tokens_data = await refresh_use_case(refresh_token)
    
    response.set_cookie(
        key="access_token",
        value=user_tokens_data.access_token.token,
        httponly=True,
        secure=False,  # TODO: В продакшн с HTTPS
        samesite="lax",
        expires=settings.access_token.token_lifetime_minutes * 60,
        path="/"
    )
    
    response.set_cookie(
        key="refresh_token",
        value=user_tokens_data.refresh_token.token,
        httponly=True,
        secure=False,  # TODO: В продакшн с HTTPS
        samesite="lax",
        expires=settings.refresh_token.token_lifetime_days * 24 * 60 * 60,
        path="/"
    )
    
    return user_tokens_data.user