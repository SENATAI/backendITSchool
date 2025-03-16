from jose import JWTError, jwt
import logging
from uuid import UUID
from datetime import datetime
from ..schemas import UserTokenDataReadSchema
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.core.enums import UserRole
from school_site.settings import settings

logger = logging.getLogger(__name__)


class AuthServiceProtocol:
    async def get_admin_user(self, token: str) -> UserTokenDataReadSchema:
        ...


class AuthService(AuthServiceProtocol):
    async def decode_access_token(self, token: str) -> UserTokenDataReadSchema:
        logger.info("Decoding access token")

        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt.token_algorithm])
            user_id_str = payload.get("user_id")
            role = payload.get("role")
            exp = payload.get("exp")

            if user_id_str is None:
                logger.error("Invalid token: missing user_id")
                raise PermissionDeniedError()

            try:
                user_id = UUID(user_id_str)
            except ValueError:
                logger.error("Invalid token: user_id not a valid UUID")
                raise PermissionDeniedError()

            if exp is None:
                logger.error("Invalid token: missing expiration time")
                raise PermissionDeniedError()

            try:
                role_enum = UserRole(role)
            except ValueError:
                logger.error(f"Invalid token: unknown role {role}")
                raise PermissionDeniedError()

            token_data = UserTokenDataReadSchema(
                user_id=user_id,
                role=role_enum,
                expiration=datetime.fromtimestamp(exp)
            )
            logger.info(f"Token decoded successfully for user: {user_id}")

            return token_data

        except JWTError as e:
            logger.warning("Failed to decode token", exc_info=True)
            raise PermissionDeniedError()

    async def get_admin_user(self, access_token: str) -> UserTokenDataReadSchema:
        user_data = await self.decode_access_token(access_token)
        if user_data.role != UserRole.ADMINISTRATOR:
            logger.error("User is not an admin")
            raise PermissionDeniedError()
        return user_data
