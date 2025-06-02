import argparse
import asyncio
from contextlib import asynccontextmanager
from passlib.context import CryptContext
from uuid import UUID
from school_site.apps.teachers.repositories.teachers import TeacherRepository
from school_site.apps.teachers.schemas import TeacherCreateSchema
from school_site.core.db import get_async_session  
from school_site.apps.users.services.users import UserService  
from school_site.apps.users.repositories.users import UserRepository
from school_site.apps.users.schemas import RegisterRequestSchema
from school_site.core.enums import UserRole
from school_site.apps.students.schemas import StudentCreateSchema
from school_site.apps.students.repositories.students import StudentRepository
from school_site.apps.users.services.passwords import PasswordService 
from school_site.apps.groups.services.group_students import GroupStudentService
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

        # Если пользователь - учитель, создаем запись учителя
        if new_user.role == UserRole.TEACHER:
            teacher_repo = TeacherRepository(session)
            teacher_schema = TeacherCreateSchema(user_id=new_user.id)
            new_teacher = await teacher_repo.create(teacher_schema)
            print(f"Учитель создан: {new_teacher}")


if __name__ == "__main__":
    asyncio.run(main())
