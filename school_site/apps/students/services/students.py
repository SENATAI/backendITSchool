from uuid import UUID
from typing import Protocol
from school_site.core.schemas import PaginationSchema
from ..repositories.students import StudentRepositoryProtocol
from ..schemas import StudentCreateSchema, StudentReadSchema, StudentUpdateSchema, StudentPaginationResultSchema
from ..exceptions import StudentNotExistsExceptions

class StudentServiceProtocol(Protocol):
    async def create(self, student: StudentCreateSchema) -> StudentReadSchema:
        ...

    async def get(self, student_id: UUID) -> StudentReadSchema:
        ...

    async def update(self, student_id: UUID, student: StudentUpdateSchema) -> StudentReadSchema:
        ...

    async def delete(self, student_id: UUID) -> bool:
        ...

    async def list(self, pagination: PaginationSchema) -> StudentPaginationResultSchema:
        ...

    async def get_by_user_id(self, user_id: UUID) -> StudentReadSchema:
        ...


class StudentService(StudentServiceProtocol):
    def __init__(self, student_repository: StudentRepositoryProtocol):
        self.student_repository = student_repository

    async def create(self, student: StudentCreateSchema) -> StudentReadSchema:
        return await self.student_repository.create(student)
    
    async def get(self, student_id: UUID) -> StudentReadSchema:
        return await self.student_repository.get(student_id)
    
    async def update(self, student_id: UUID, student: StudentUpdateSchema) -> StudentReadSchema:
        student_for_update = StudentUpdateSchema(
            id=student_id,
            points=student.points
        )
        return await self.student_repository.update(student_for_update)
    
    async def delete(self, student_id: UUID) -> bool:
        return await self.student_repository.delete(student_id)
    
    async def list(self, pagination: PaginationSchema) -> StudentPaginationResultSchema:
        return await self.student_repository.paginate(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            sorting=["created_at", "id"],
            policies=["can_view"]
        )
    
    async def get_by_user_id(self, user_id: UUID) -> StudentReadSchema:
        student = await self.student_repository.get_by_user_id(user_id)
        if not student:
            raise StudentNotExistsExceptions(user_id)
        return student