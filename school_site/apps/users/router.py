from fastapi import APIRouter, Depends, Response, Cookie
from .schemas import LoginRequestSchema, UserReadSchema, PasswordChangeSchema, UserResetSchema
from .use_cases.login import LoginUseCaseProtocol
from .use_cases.refresh import RefreshUseCaseProtocol
from .use_cases.logout import LogoutUseCaseProtocol
from .use_cases.change_password import ChangePasswordUseCaseProtocol
from .use_cases.reset_password import ResetPasswordUseCaseProtocol
from .depends import (
    get_login_use_case, get_refresh_use_case, get_logout_use_case, get_change_password_use_case,
    get_reset_password_use_case
)
from .utils.cookies import set_auth_cookies

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
    
    set_auth_cookies(
        response, 
        user_tokens_data.access_token.token, 
        user_tokens_data.refresh_token.token
    )
    
    return user_tokens_data.user

@router.post("/refresh", response_model=UserReadSchema)
async def refresh_token(
    response: Response,
    refresh_use_case: RefreshUseCaseProtocol = Depends(get_refresh_use_case),
    refresh_token: str = Cookie(...)
):
    user_tokens_data = await refresh_use_case(refresh_token)
    
    set_auth_cookies(
        response, 
        user_tokens_data.access_token.token, 
        user_tokens_data.refresh_token.token
    )
    
    return user_tokens_data.user

@router.post("/logout", status_code=204)
async def logout(
    response: Response,
    logout: LogoutUseCaseProtocol = Depends(get_logout_use_case),
    refresh_token: str = Cookie(...),
):
    await logout(refresh_token)
    
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    
    return None


@router.post("/change_password", response_model=UserReadSchema, status_code=200)
async def change_password(
    response: Response,
    password_data: PasswordChangeSchema,  
    change_password_use_case: ChangePasswordUseCaseProtocol = Depends(get_change_password_use_case),
    access_token: str = Cookie(...)
):
    """Смена пароля авторизованным пользователем"""
    user_tokens_data = await change_password_use_case(
        access_token, 
        password_data
    )
    set_auth_cookies(
        response, 
        user_tokens_data.access_token.token, 
        user_tokens_data.refresh_token.token
    )
    return user_tokens_data.user


@router.post("/reset_password", status_code=204)
async def reset_password(
    user: UserResetSchema,
    reset_password_use_case: ResetPasswordUseCaseProtocol = Depends(get_reset_password_use_case)
):
    await reset_password_use_case(user)
    
    return None
