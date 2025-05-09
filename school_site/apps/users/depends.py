from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from school_site.core.db import get_async_session
from school_site.apps.emails.depends import get_email_client
from school_site.apps.emails.clients.emails import EmailClientProtocol
from .schemas import CookieTokenSchema
from .repositories.users import UserRepositoryProtocol, UserRepository
from .repositories.refresh_tokens import RefreshTokenRepositoryProtocol, RefreshTokenRepository
from .repositories.reset_tokens import ResetTokenRepositoryProtocol, ResetTokenRepository
from .services.passwords import PasswordServiceProtocol, PasswordService
from .services.users import UserServiceProtocol, UserService
from .services.tokens import TokenServiceProtocol, TokenService, ResetPasswordTokenServiceProtocol, ResetPasswordTokenService
from .services.auth import AuthServiceProtocol, AuthService, ResetPasswordServiceProtocol, ResetPasswordService
from .use_cases.login import LoginUseCaseProtocol, LoginUseCase
from .use_cases.refresh import RefreshUseCaseProtocol, RefreshUseCase
from .use_cases.logout import LogoutUseCaseProtocol, LogoutUseCase
from .use_cases.change_password import ChangePasswordUseCaseProtocol, ChangePasswordUseCase
from .use_cases.reset_password import ResetPasswordUseCaseProtocol, ResetPasswordUseCase


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

def __get_reset_password_repository(
    session: AsyncSession = Depends(get_async_session)
) -> ResetTokenRepositoryProtocol:
    return ResetTokenRepository(session)


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


def get_reset_password_token_service(token_repository: ResetTokenRepositoryProtocol = Depends(__get_reset_password_repository),
                                     password_service: PasswordServiceProtocol = Depends(get_password_service)
                                     ) -> ResetPasswordTokenServiceProtocol:
    return ResetPasswordTokenService(token_repository, password_service)

def get_reset_password_service(user_service: UserServiceProtocol = Depends(get_user_service),
                               mail_sender: EmailClientProtocol = Depends(get_email_client),
                               reset_password_service: ResetPasswordTokenServiceProtocol = Depends(get_reset_password_token_service)) -> \
    ResetPasswordServiceProtocol:
    return ResetPasswordService(user_service, mail_sender, reset_password_service)

def get_reset_password_use_case(reset_password_service: ResetPasswordServiceProtocol = Depends(get_reset_password_service)) -> \
    ResetPasswordUseCaseProtocol:
    return ResetPasswordUseCase(reset_password_service)

access_token_schema = CookieTokenSchema(cookie_name="access_token")
refresh_token_schema = CookieTokenSchema(cookie_name="refresh_token")