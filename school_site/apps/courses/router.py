from fastapi import APIRouter, Depends, Path, Query, UploadFile, File, Form
from school_site.apps.users.depends import access_token_schema
from uuid import UUID
from typing import Optional
from .use_cases.create_course import CreateCourseUseCaseProtocol
from .use_cases.update_course import UpdateCourseUseCaseProtocol
from .use_cases.get_course import GetCourseUseCaseProtocol
from .use_cases.delete_course import DeleteCourseUseCaseProtocol
from .use_cases.list_courses import GetListCoursesUseCaseProtocol
from .use_cases.create_lesson import CreateLessonUseCaseProtocol
from .use_cases.update_lesson import UpdateLessonUseCaseProtocol
from .use_cases.get_lesson import GetLessonUseCaseProtocol
from .use_cases.delete_lesson import DeleteLessonUseCaseProtocol
from .use_cases.list_lessons import GetListLessonsUseCaseProtocol
from .use_cases.create_material import CreateLessonHTMLFileUseCaseProtocol
from .depends import (
    get_course_create_use_case, get_course_update_use_case, get_course_get_use_case,
    get_course_delete_use_case, get_course_get_list_use_case,
    get_lesson_create_use_case, get_lesson_update_use_case, get_lesson_get_use_case,
    get_lesson_delete_use_case, get_lesson_get_list_use_case, get_material_create_use_case
)
from .schemas import (
    CourseWithPhotoReadSchema, CourseWithPhotoPaginationResultSchema,
    LessonReadSchema, LessonPaginationResultSchema, LessonCreateSchema, LessonUpdateSchema,
    LessonWithMaterialsCreateSchema, LessonHTMLCreateSchema, LessonWithMaterialsReadSchema
)

router = APIRouter(prefix='/api/courses', tags=['Courses'])


@router.post("/", response_model=CourseWithPhotoReadSchema, status_code=201)
async def create_course(
    course_data: str = Form(...),
    create: CreateCourseUseCaseProtocol = Depends(get_course_create_use_case),
    image: Optional[UploadFile] = File(None),
    access_token: str = Depends(access_token_schema)
):
    created_course = await create(course_data, image, access_token)
    return created_course


@router.put("/{course_id}", response_model=CourseWithPhotoReadSchema, status_code=200)
async def update_course(
    course_data: str = Form(...),
    course_id: UUID = Path(...),
    update: UpdateCourseUseCaseProtocol = Depends(get_course_update_use_case),
    image: Optional[UploadFile] = File(None),
    access_token: str = Depends(access_token_schema)
):
    updated_course = await update(course_id, course_data, image, access_token)
    return updated_course


@router.get("/{course_id}", response_model=CourseWithPhotoReadSchema, status_code=200)
async def get_course(
    course_id: UUID = Path(...),
    get: GetCourseUseCaseProtocol = Depends(get_course_get_use_case)
):
    course = await get(course_id)
    return course


@router.get("/", response_model=CourseWithPhotoPaginationResultSchema, status_code=200)
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
    delete: DeleteCourseUseCaseProtocol = Depends(get_course_delete_use_case),
    access_token: str = Depends(access_token_schema)
):
    await delete(course_id, access_token)
    return None


@router.post("/{course_id}/lessons", response_model=LessonReadSchema, status_code=201)
async def create_lesson(
    lesson: LessonCreateSchema,
    course_id: UUID = Path(...),
    create: CreateLessonUseCaseProtocol = Depends(get_lesson_create_use_case),
    access_token: str = Depends(access_token_schema)
):
    created_lesson = await create(course_id, lesson, access_token)
    return created_lesson


@router.put("/{course_id}/lessons/{lesson_id}", response_model=LessonReadSchema, status_code=200)
async def update_lesson(
    lesson: LessonUpdateSchema,
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    update: UpdateLessonUseCaseProtocol = Depends(get_lesson_update_use_case),
    access_token: str = Depends(access_token_schema)
):
    updated_lesson = await update(course_id, lesson_id, lesson, access_token)
    return updated_lesson


@router.get("/{course_id}/lessons/{lesson_id}", response_model=LessonReadSchema, status_code=200)
async def get_lesson(
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    get: GetLessonUseCaseProtocol = Depends(get_lesson_get_use_case)
):
    lesson = await get(course_id, lesson_id)
    return lesson


@router.get("/{course_id}/lessons", response_model=LessonPaginationResultSchema, status_code=200)
async def list_lessons(
    course_id: UUID = Path(...),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    list: GetListLessonsUseCaseProtocol = Depends(get_lesson_get_list_use_case)
):
    lessons = await list(course_id, limit, offset)
    return lessons


@router.delete("/{course_id}/lessons/{lesson_id}", status_code=204)
async def delete_lesson(
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    delete: DeleteLessonUseCaseProtocol = Depends(get_lesson_delete_use_case),
    access_token: str = Depends(access_token_schema)
):
    await delete(course_id, lesson_id, access_token)
    return None


@router.post("/{course_id}/lessons-with-materials", response_model=LessonWithMaterialsReadSchema, status_code=201)
async def create_lesson_with_materials(
    data: LessonWithMaterialsCreateSchema,
    course_id: UUID = Path(...),
    lesson_create_use_case: CreateLessonUseCaseProtocol = Depends(get_lesson_create_use_case),
    material_create_use_case: CreateLessonHTMLFileUseCaseProtocol = Depends(get_material_create_use_case),
    access_token: str = Depends(access_token_schema)
):
    teacher_material = LessonHTMLCreateSchema(name=data.teacher_material_name, html_text=data.teacher_material_text)
    student_material = LessonHTMLCreateSchema(name=data.student_material_name, html_text=data.student_material_text)
    homework = LessonHTMLCreateSchema(name=data.homework_material_name, html_text=data.homework_material_text)
    
    created_teacher_material= await material_create_use_case(teacher_material, access_token)
    created_student_material = await material_create_use_case(student_material, access_token)
    created_homework = await  material_create_use_case(homework, access_token)

    lesson = LessonCreateSchema(name=data.name, teacher_material_id=created_teacher_material.id, 
                                student_material_id=created_student_material.id, homework_id=created_homework.id)

    created_lesson = await lesson_create_use_case(
        course_id,
        lesson,
        access_token
    )
    return LessonWithMaterialsReadSchema(
        id=created_lesson.id, 
        course_id=created_lesson.course_id,
        name=created_lesson.name, 
        teacher_material_id=created_teacher_material.id,
        student_material_id=created_student_material.id, 
        homework_id=created_homework.id,
        teacher_material_url=created_teacher_material.url,
        student_material_url=created_student_material.url,
        homework_material_url=created_homework.url
        )