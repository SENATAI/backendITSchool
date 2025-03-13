import logging
from typing import Protocol
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

class PasswordServiceProtocol(Protocol):
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        ...
    
    def get_password_hash(self, password: str) -> str:
        ...


class PasswordService(PasswordServiceProtocol):
    def __init__(self, pwd_context: CryptContext):
        self.pwd_context = pwd_context

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        logger.info("Verifying password")
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        logger.info("Generating password hash")
        return self.pwd_context.hash(password)

