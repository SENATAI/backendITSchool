from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from school_site.core.db import get_async_session
from .repositories.users import UserRepositoryProtocol, UserRepository
from .repositories.refresh_tokens import RefreshTokenRepositoryProtocol, RefreshTokenRepository
from .services.passwords import PasswordServiceProtocol, PasswordService
from .services.users import UserServiceProtocol, UserService
from .services.tokens import TokenServiceProtocol, TokenService
from .services.auth import AuthServiceProtocol, AuthService
from .use_cases.login import LoginUseCaseProtocol, LoginUseCase
from .use_cases.refresh import RefreshUseCaseProtocol, RefreshUseCase
from .use_cases.logout import LogoutUseCaseProtocol, LogoutUseCase
from .use_cases.change_password import ChangePasswordUseCaseProtocol, ChangePasswordUseCase


def __get_user_repository(
        session: AsyncSession = Depends(get_async_session)
) -> UserRepositoryProtocol:
    return UserRepository(session)


def __get_refresh_tokens_repository(
        session: AsyncSession = Depends(get_async_session)
) -> RefreshTokenRepositoryProtocol:
    return RefreshTokenRepository(session)


def __get_pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_service(pwd_context: CryptContext = Depends(__get_pwd_context)) -> PasswordServiceProtocol:
    return PasswordService(pwd_context)


def get_user_service(user_repository: UserRepositoryProtocol = Depends(__get_user_repository),
        password_service: PasswordServiceProtocol = Depends(get_password_service)                    
) -> UserServiceProtocol:
    return UserService(user_repository, password_service)


def get_token_service(token_repository: RefreshTokenRepositoryProtocol = Depends(__get_refresh_tokens_repository)) -> \
    TokenServiceProtocol:
    return TokenService(token_repository)


def get_auth_service(user_service: UserServiceProtocol = Depends(get_user_service),
                     token_service: TokenServiceProtocol = Depends(get_token_service)) -> AuthServiceProtocol:
    return AuthService(user_service, token_service)


def get_login_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> LoginUseCaseProtocol:
    return LoginUseCase(auth_service)


def get_refresh_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> RefreshUseCaseProtocol:
    return RefreshUseCase(auth_service)


def get_logout_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> LogoutUseCaseProtocol:
    return LogoutUseCase(auth_service)

def get_change_password_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> ChangePasswordUseCaseProtocol:
    return ChangePasswordUseCase(auth_service)