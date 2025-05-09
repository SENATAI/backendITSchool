import logging
from typing import Protocol, Self
from uuid import UUID
from school_site.core.enums import UserRole
from ..texts import HTML_EMAIL_BODY_TEMPLATE, HTML_EMAIL_SUBJECT_TEMPLATE
from ..schemas import AuthReadSchema, PasswordChangeSchema, UserResetSchema, UserReadSchema, ResetTokenSchema
from .users import UserServiceProtocol
from .tokens import TokenServiceProtocol, ResetPasswordTokenServiceProtocol
from school_site.apps.emails.clients.emails import EmailClientProtocol
from school_site.apps.emails.schemas import EmailRequestDTO
from school_site.settings import settings

logger = logging.getLogger(__name__)


class AuthServiceProtocol(Protocol):
    async def login(self: Self, username: str, password: str) -> AuthReadSchema:
        ...
    
    async def refresh(self: Self, refresh_token: str) -> AuthReadSchema:
        ...

    async def logout(self: Self, refresh_token: str) -> None:
        ...

    async def change_password(self: Self, access_token: str, password: PasswordChangeSchema) -> AuthReadSchema:
        ...
class AuthService(AuthServiceProtocol):
    def __init__(
        self: Self,
        user_service: UserServiceProtocol,
        token_service: TokenServiceProtocol,
    ):
        self.user_service = user_service
        self.token_service = token_service
    
    async def change_password(self: Self, access_token: str, password: PasswordChangeSchema) -> AuthReadSchema:
        user_data = await self.token_service.decode_access_token(access_token)
        await self.user_service.authenticate_user_by_id(user_data.user_id, password.old_password)
        updated_user = await self.user_service.change_password(user_data.user_id, password.new_password)
        await self.token_service.delete_all_by_user_id(updated_user.id)
        new_access_token, new_refresh_data = await self._create_tokens(updated_user.id, updated_user.role)

        return AuthReadSchema(user=updated_user,
                              access_token=new_access_token,
                              refresh_token=new_refresh_data)
    
    async def login(self: Self, username: str, password: str) -> AuthReadSchema:
        logger.info(f"Login attempt for user: {username}")
        
        user = await self.user_service.authenticate_user(username, password)
        
        access_token, refresh_data = await self._create_tokens(user.id, user.role)
        
        logger.info(f"Login successful for user: {username}")
        
        return AuthReadSchema(user=user,
                              access_token=access_token,
                              refresh_token=refresh_data)
    
    async def _create_tokens(self: Self, user_id: UUID, role: UserRole) -> tuple[str, str]:
        access_token = self.token_service.create_access_token(
            user_id=user_id, 
            role=role, 
        )
        
        refresh_data = await self.token_service.create_refresh_token(user_id)

        return access_token, refresh_data
    
    async def refresh(self: Self, refresh_token: str) -> AuthReadSchema:
        logger.info("Refreshing tokens")
        
        db_token = await self.token_service.verify_refresh_token(refresh_token)
        
        user = await self.user_service.get_user_by_id(db_token.user_id)
        
        await self.token_service.delete(db_token.id)
        
        access_token = self.token_service.create_access_token(
            user_id=user.id, 
            role=user.role, 
        )
        
        new_refresh_data = await self.token_service.create_refresh_token(user.id)
        
        logger.info(f"Tokens refreshed successfully for user: {user.id}")
        
        return AuthReadSchema(user=user,
                              access_token=access_token,
                              refresh_token=new_refresh_data)
    
    
    async def logout(self: Self, refresh_token: str) -> None:
        db_token = await self.token_service.verify_refresh_token(refresh_token)
        user_id = db_token.user_id
        logger.info(f"Logout for user: {user_id}")
        if db_token:
            await self.token_service.delete(db_token.id)
            logger.info(f"Refresh token removed for user: {user_id}")
        
        logger.info(f"Logout successful for user: {user_id}")

    
    

class ResetPasswordServiceProtocol(Protocol):
    async def reset_password(self: Self, user: UserResetSchema) -> bool:
        ...


class ResetPasswordService(ResetPasswordServiceProtocol):
    def __init__(self: Self, user_service: UserServiceProtocol,
                 mail_sender: EmailClientProtocol,
                reset_password_token_service: ResetPasswordTokenServiceProtocol):
        self.user_service = user_service
        self.reset_password_token_service = reset_password_token_service
        self.mail_sender = mail_sender

    async def reset_password(self: Self, user: UserResetSchema) -> bool:
        logger.info(f"Resetting password for user: {user.email}")
        user_data = await self.user_service.get_by_email_or_none(user.email)
        if user_data:
            token = await self.reset_password_token_service.generate_reset_token(user_data.id)
            message = self._generate_email_message(user_data, token)
            print(message)
            await self.mail_sender.send_email(message)
        return True

    def _generate_email_message(self: Self, user: UserReadSchema, token: ResetTokenSchema) -> str:
        name = user.first_name or user.username
        
        body =  HTML_EMAIL_BODY_TEMPLATE.format(
            name=name,
            url=settings.frontend_url,
            token=token.token,
            duration=token.hours
        )

        subject = HTML_EMAIL_SUBJECT_TEMPLATE.strip()

        return EmailRequestDTO(
            to_email=user.email,
            body=body,
            subject=subject
        )




