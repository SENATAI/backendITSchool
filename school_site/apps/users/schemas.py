from pydantic import BaseModel, EmailStr, field_validator
import re
from typing import Optional
from uuid import UUID
from datetime import datetime
from school_site.core.schemas import CreateBaseModel, UpdateBaseModel
from school_site.core.enums import UserRole

class LoginRequestSchema(BaseModel):
    username: str
    password: str


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str

class PasswordSchema(BaseModel):
    password_hash: str

class PhoneValidatedMixin(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        pattern = r"^\+?[0-9]{10,15}$"
        if not re.match(pattern, v):
            raise ValueError("Неверный формат номера телефона. Пример: +79991234567")
        return v

    class Config:
        arbitrary_types_allowed = True


class UserInfoMixin(BaseModel):
    first_name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    email: EmailStr
    role: UserRole
    username: str



class RegisterRequestSchema(PhoneValidatedMixin, UserInfoMixin):
    password: str


class UserCreateSchema(PhoneValidatedMixin, UserInfoMixin, CreateBaseModel):
    password_hash: str


class UserUpdateDBSchema(PhoneValidatedMixin, UserInfoMixin, UpdateBaseModel):
    password_hash: str


class UserUpdateSchema(PhoneValidatedMixin, UserInfoMixin, UpdateBaseModel):
    password: str


class UserReadSchema(PhoneValidatedMixin, UserInfoMixin):
    id: UUID


class UserReadDBSchema(PhoneValidatedMixin, UserInfoMixin):
    id: UUID
    password_hash: str


class UserTokenDataReadSchema(BaseModel):
    user_id: UUID
    role: UserRole
    expiration: datetime


class TokenReadSchema(BaseModel):
    token: str
    expiration: datetime


class RefreshTokenReadDBSchema(BaseModel):
    id: UUID
    user_id: UUID
    hashed_refresh_token: str
    created_at: datetime


class RefreshTokenUpdateDBSchema(BaseModel):
    id: UUID
    user_id: UUID
    hashed_refresh_token: str


class RefreshTokenCreateDBSchema(CreateBaseModel):
    user_id: UUID
    hashed_refresh_token: str


class AuthReadSchema(BaseModel):
    user: UserReadSchema
    access_token: TokenReadSchema
    refresh_token: TokenReadSchema

class UserUpdateRequestSchema(PhoneValidatedMixin, UserInfoMixin, BaseModel):  
    password: str | None = None