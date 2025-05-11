import argparse
import asyncio
from contextlib import asynccontextmanager
from passlib.context import CryptContext
from uuid import UUID
from school_site.core.db import get_async_session  
from school_site.apps.users.services.users import UserService  
from school_site.apps.users.repositories.users import UserRepository
from school_site.apps.users.schemas import RegisterRequestSchema
from school_site.core.enums import UserRole
from school_site.apps.students.schemas import StudentCreateSchema
from school_site.apps.students.repositories.students import StudentRepository
from school_site.apps.users.services.passwords import PasswordService 
from school_site.apps.groups.services.students import GroupStudentService
from school_site.apps.groups.repositories.group_students import GroupStudentsRepository
from school_site.apps.students.services.students import StudentService
from school_site.apps.groups.schemas import GroupAddStudentsSchema


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
    parser.add_argument("--first_name", required=False, help="Имя пользователя", default=None)
    parser.add_argument("--surname", required=False, help="Фамилия пользователя", default=None)
    parser.add_argument("--patronymic", required=False, help="Отчество пользователя", default=None)
    parser.add_argument("--email", required=True, help="Email пользователя")
    parser.add_argument("--phone_number", required=True, help="Телефонный номер пользователя")
    parser.add_argument("--points", required=False, help="Очки пользователя", default=0)
    parser.add_argument("--group_id", required=False, help="ID группы для добавления студента", default=None)

    args = parser.parse_args()

    async with get_session() as session:
        # Создание пользователя
        user_repository = UserRepository(session)
        password_service = PasswordService(CryptContext(schemes=["bcrypt"], deprecated="auto"))
        user_service = UserService(user_repository, password_service)
        user_data = RegisterRequestSchema(
            username=args.username, 
            password=args.password, 
            role=args.role,
            first_name=args.first_name,
            surname=args.surname,
            patronymic=args.patronymic,
            email=args.email,
            phone_number=args.phone_number
        )
        new_user = await user_service.create_user(user_data)
        print(f"Пользователь создан: {new_user}")

        # Если пользователь - студент, создаем запись студента
        if new_user.role == UserRole.STUDENT:
            st_repo = StudentRepository(session)
            st_schema = StudentCreateSchema(
                user_id=new_user.id,
                points=int(args.points)
            )
            new_student = await st_repo.create(st_schema)
            print(f"Студент создан: {new_student}")

            # Если указан ID группы, добавляем студента в группу
            if args.group_id:
                group_students_repository = GroupStudentsRepository(session)
                student_service = StudentService(st_repo)
                group_student_service = GroupStudentService(group_students_repository, student_service)
                students_data = GroupAddStudentsSchema(students_id=[new_student.id])
                await group_student_service.add_students(UUID(args.group_id), students_data)
                print(f"Студент добавлен в группу с ID: {args.group_id}")

if __name__ == "__main__":
    asyncio.run(main())
