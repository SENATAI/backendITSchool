from fastapi import APIRouter, Depends, Path, Query
from uuid import UUID
from .use_cases.create_course import CreateCourseUseCaseProtocol
from .use_cases.update_course import UpdateCourseUseCaseProtocol
from .use_cases.get_course import GetCourseUseCaseProtocol
from .use_cases.delete_course import DeleteCourseUseCaseProtocol
from .use_cases.list_courses import GetListCoursesUseCaseProtocol
from .depends import (
    get_course_create_use_case, get_course_update_use_case, get_course_get_use_case,
    get_course_delete_use_case, get_course_get_list_use_case
)
from .schemas import CourseReadSchema, CoursePaginationResultSchema, CourseCreateSchema, CourseUpdateSchema

router = APIRouter(prefix='/api/courses', tags=['Courses'])


@router.post("/", response_model=CourseReadSchema, status_code=201)
async def create_course(
    course_data: CourseCreateSchema,
    create: CreateCourseUseCaseProtocol = Depends(get_course_create_use_case)
):
    created_course = await create(course_data)
    return created_course


@router.put("/{course_id}", response_model=CourseReadSchema, status_code=200)
async def update_course(
    course_data: CourseUpdateSchema,
    course_id: UUID = Path(...),
    update: UpdateCourseUseCaseProtocol = Depends(get_course_update_use_case)
):
    updated_course = await update(course_id, course_data)
    return updated_course


@router.get("/{course_id}", response_model=CourseReadSchema, status_code=200)
async def get_course(
    course_id: UUID = Path(...),
    get: GetCourseUseCaseProtocol = Depends(get_course_get_use_case)
):
    course = await get(course_id)
    return course


@router.get("/", response_model=CoursePaginationResultSchema, status_code=200)
async def list_courses(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    list: GetListCoursesUseCaseProtocol = Depends(get_course_get_list_use_case)
):
    courses = await list(limit, offset)
    return courses


@router.delete("/{course_id}", status_code=204)
async def delete_course(
    course_id: UUID = Path(...),
    delete: DeleteCourseUseCaseProtocol = Depends(get_course_delete_use_case)
):
    await delete(course_id)
    return None
