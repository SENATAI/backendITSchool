from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import PasswordResetTokens
from ..schemas import ResetTokenCreateSchema, ResetTokenUpdateSchema, ResetTokenReadSchema


class ResetTokenRepositoryProtocol(BaseRepositoryImpl[
    PasswordResetTokens,
    ResetTokenReadSchema,
    ResetTokenCreateSchema,
    ResetTokenUpdateSchema
]):
    pass

class ResetTokenRepository(ResetTokenRepositoryProtocol):
    pass