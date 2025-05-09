from fastapi import APIRouter, Depends, Response, Cookie
from typing import List
from uuid import UUID
from .schemas import LoginRequestSchema, UserReadSchema, PasswordChangeSchema, RegisterRequestSchema, UserUpdateSchema
from .use_cases.login import LoginUseCaseProtocol
from .use_cases.refresh import RefreshUseCaseProtocol
from .use_cases.logout import LogoutUseCaseProtocol
from .use_cases.change_password import ChangePasswordUseCaseProtocol
from .use_cases.create_user import CreateUserUseCaseProtocol
from .use_cases.get_all_users import GetAllUsersUseCaseProtocol
from .use_cases.get_user_by_id import GetUserByIdUseCaseProtocol
from .use_cases.update_user import UpdateUserUseCaseProtocol
from .use_cases.delete_user import DeleteUserUseCaseProtocol
from .depends import get_login_use_case, get_refresh_use_case, get_logout_use_case, get_change_password_use_case, get_create_user_use_case, get_all_users_use_case, get_get_user_by_id_use_case, get_update_user_use_case, get_delete_user_use_case
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


@router.post("/", response_model=UserReadSchema, status_code=201)
async def create_user(
    user_data: RegisterRequestSchema,
    create_user_use_case: CreateUserUseCaseProtocol = Depends(get_create_user_use_case)
):
    return await create_user_use_case(user_data)
    

@router.get("/", response_model=List[UserReadSchema], status_code=200)
async def get_all_users(
    get_all_users_use_case: GetAllUsersUseCaseProtocol = Depends(get_all_users_use_case)
):
    return await get_all_users_use_case()

@router.get("/{user_id}", response_model=UserReadSchema, status_code=200)
async def get_user_by_id(
    user_id: UUID,
    get_user_by_id_use_case: GetUserByIdUseCaseProtocol = Depends(get_get_user_by_id_use_case)
):
    return await get_user_by_id_use_case(user_id)

@router.put("/{user_id}", response_model=UserReadSchema, status_code=200)
async def update_user2(
    user_id: UUID, 
    user_data: UserUpdateSchema,
    update_user_use_case: UpdateUserUseCaseProtocol = Depends(get_update_user_use_case)
):
    return await update_user_use_case(user_id, user_data)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    delete_user_use_case: DeleteUserUseCaseProtocol = Depends(get_delete_user_use_case)
):
    await delete_user_use_case(user_id)
    return None