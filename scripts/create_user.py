import argparse
import asyncio
from contextlib import asynccontextmanager
from passlib.context import CryptContext

from school_site.core.db import get_async_session  
from school_site.apps.users.services.users import UserService  
from school_site.apps.users.repositories.users import UserRepository
from school_site.apps.users.schemas import RegisterRequestSchema
from school_site.core.enums import UserRole
from school_site.apps.students.schemas import StudentCreateSchema
from school_site.apps.students.repositories.students import StudentRepository
from school_site.apps.users.services.passwords import PasswordService 


@asynccontextmanager
async def get_session():
    session_gen = get_async_session()
    session = await session_gen.__anext__()
    try:
        yield session
    finally:
        await session_gen.aclose()

async def main():
    parser = argparse.ArgumentParser(description="Создание нового пользователя")
    parser.add_argument("--username", required=True, help="Имя пользователя")
    parser.add_argument("--password", required=True, help="Пароль пользователя")
    parser.add_argument("--role", required=True, help="Роль пользователя")
    parser.add_argument("--points", required=False, help="Очки пользователя", default=0)

    args = parser.parse_args()

    async with get_session() as session:
        user_repository = UserRepository(session)
        password_service = PasswordService(CryptContext(schemes=["bcrypt"], deprecated="auto"))
        user_service = UserService(user_repository, password_service)
        user_data = RegisterRequestSchema(username=args.username, password=args.password, role=args.role)
        new_user = await user_service.create_user(user_data)
        if new_user.role == UserRole.STUDENT:
            st_repo = StudentRepository(session)
            st_schema = StudentCreateSchema(
                user_id=new_user.id,
                points=int(args.points)
            )
            new_st = await st_repo.create(st_schema) 
            print(f"Студент создан: {new_st}")

        print(f"Пользователь создан: {new_user}")

if __name__ == "__main__":
    asyncio.run(main())
