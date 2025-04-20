from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from school_site.core.schemas import CreateBaseModel, UpdateBaseModel
from school_site.core.enums import UserRole

class LoginRequestSchema(BaseModel):
    username: str
    password: str

class RegisterRequestSchema(BaseModel):
    username: str
    password: str
    role: str


class UserCreateSchema(CreateBaseModel):
    username: str
    password_hash: str
    role: UserRole


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str

class UserUpdateDBSchema(UpdateBaseModel):
    username: str
    hash_password: str
    role: UserRole

class UserUpdateSchema(UpdateBaseModel):
    username: str
    password: str
    role: UserRole

class UserReadSchema(BaseModel):
    id: UUID
    username: str
    role: UserRole


class UserReadDBSchema(BaseModel):
    id: UUID
    username: str
    password_hash: str
    role: UserRole


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