from fastapi import APIRouter, Depends, Path, Query, UploadFile, File, Form
from school_site.apps.users.depends import access_token_schema
from uuid import UUID
from typing import Optional
from .use_cases.courses.create_course import CreateCourseUseCaseProtocol
from .use_cases.courses.update_course import UpdateCourseUseCaseProtocol
from .use_cases.courses.get_course import GetCourseUseCaseProtocol
from .use_cases.courses.delete_course import DeleteCourseUseCaseProtocol
from .use_cases.courses.list_courses import GetListCoursesUseCaseProtocol
from .use_cases.lessons.create_lesson import CreateLessonUseCaseProtocol
from .use_cases.lessons.update_lesson import UpdateLessonUseCaseProtocol
from .use_cases.lessons.get_lesson import GetLessonUseCaseProtocol
from .use_cases.lessons.delete_lesson import DeleteLessonUseCaseProtocol
from .use_cases.lessons.list_lessons import GetListLessonsUseCaseProtocol
from .use_cases.materials.create_material import CreateLessonHTMLFileUseCaseProtocol
from .use_cases.materials.update_material import UpdateLessonHTMLFileUseCaseProtocol
from .use_cases.materials.get_material import GetLessonHTMLFileUseCaseProtocol
from .use_cases.materials.delete_material import DeleteLessonHTMLFileUseCaseProtocol
from .use_cases.lesson_group_student.create_lesson_group_student import CreateLessonGroupStudentUseCaseProtocol, CreateLessonGroupStudentUseCase
from .use_cases.lesson_group_student.bulk_create_lesson_group_student import BulkCreateLessonGroupStudentUseCaseProtocol, BulkCreateLessonGroupStudentUseCase
from .depends import (
    get_course_create_use_case, get_course_update_use_case, get_course_get_use_case,
    get_course_delete_use_case, get_course_get_list_use_case,
    get_lesson_create_use_case, get_lesson_update_use_case, get_lesson_get_use_case,
    get_lesson_delete_use_case, get_lesson_get_list_use_case, get_material_create_use_case,
    get_material_update_use_case, get_material_get_use_case, get_material_delete_use_case,
    get_create_lesson_group_student_use_case, get_bulk_create_lesson_group_student_use_case
)
from .schemas import (
    CourseWithPhotoReadSchema, CourseWithPhotoPaginationResultSchema,
    LessonReadSchema, LessonPaginationResultSchema, LessonCreateSchema, LessonUpdateSchema,
    LessonWithMaterialsCreateSchema, LessonWithMaterialsUpdateSchema, LessonHTMLCreateSchema, 
    LessonHTMLUpdateSchema, LessonWithMaterialsReadSchema, LessonWithMaterialsDeleteSchema,
    LessonGroupReadSchema, LessonGroupCreateSchema
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


@router.put("/{course_id}/lessons-with-materials/{lesson_id}", response_model=LessonWithMaterialsReadSchema, status_code=200)
async def update_lesson_with_materials(
    data: LessonWithMaterialsUpdateSchema,
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    lesson_update_use_case: UpdateLessonUseCaseProtocol = Depends(get_lesson_update_use_case),
    material_update_use_case: UpdateLessonHTMLFileUseCaseProtocol = Depends(get_material_update_use_case),
    access_token: str = Depends(access_token_schema)
):
    teacher_material = LessonHTMLUpdateSchema(name=data.teacher_material_name, html_text=data.teacher_material_text)
    student_material = LessonHTMLUpdateSchema(name=data.student_material_name, html_text=data.student_material_text)
    homework = LessonHTMLUpdateSchema(name=data.homework_material_name, html_text=data.homework_material_text)
    
    updated_teacher_material= await material_update_use_case(data.teacher_material_id, teacher_material, access_token)
    updated_student_material = await material_update_use_case(data.student_material_id, student_material, access_token)
    updated_homework = await  material_update_use_case(data.homework_material_id, homework, access_token)

    lesson = LessonUpdateSchema(name=data.name, teacher_material_id=updated_teacher_material.id, 
                                student_material_id=updated_student_material.id, homework_id=updated_homework.id)

    updated_lesson = await lesson_update_use_case(
        course_id,
        lesson_id,
        lesson,
        access_token
    )
    return LessonWithMaterialsReadSchema(
        id=updated_lesson.id, 
        course_id=updated_lesson.course_id,
        name=updated_lesson.name, 
        teacher_material_id=updated_teacher_material.id,
        student_material_id=updated_student_material.id, 
        homework_id=updated_homework.id,
        teacher_material_url=updated_teacher_material.url,
        student_material_url=updated_student_material.url,
        homework_material_url=updated_homework.url
        )

@router.get("/{course_id}/lessons-with-materials/{lesson_id}", response_model=LessonWithMaterialsReadSchema, status_code=200)
async def get_lesson_with_materials(
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    get_lesson: GetLessonUseCaseProtocol = Depends(get_lesson_get_use_case),
    get_material: GetLessonHTMLFileUseCaseProtocol = Depends(get_material_get_use_case),
    access_token: str = Depends(access_token_schema)
):
    lesson = await get_lesson(course_id, lesson_id)
    
    teacher_material = await get_material(lesson.teacher_material_id, access_token)
    student_material = await get_material(lesson.student_material_id, access_token)
    homework = await get_material(lesson.homework_id, access_token)


    return LessonWithMaterialsReadSchema(
        id=lesson.id, 
        course_id=lesson.course_id,
        name=lesson.name, 
        teacher_material_id=teacher_material.id,
        student_material_id=student_material.id, 
        homework_id=homework.id,
        teacher_material_url=teacher_material.url,
        student_material_url=student_material.url,
        homework_material_url=homework.url
        )


@router.delete("/{course_id}/lessons-with-materials/{lesson_id}", status_code=204)
async def delete_lesson_with_materials(
    data: LessonWithMaterialsDeleteSchema,
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    delete_lesson: DeleteLessonUseCaseProtocol = Depends(get_lesson_delete_use_case),
    delete_material: DeleteLessonHTMLFileUseCaseProtocol = Depends(get_material_delete_use_case),
    access_token: str = Depends(access_token_schema)
):
    await delete_lesson(course_id, lesson_id, access_token)
    
    await delete_material(data.teacher_material_id, access_token)
    await delete_material(data.student_material_id, access_token)
    await delete_material(data.homework_material_id, access_token)


    return None


@router.post("/lesson-group", response_model=LessonGroupReadSchema)
async def create_group_with_students(
    data: LessonGroupCreateSchema,
    create: CreateLessonGroupStudentUseCaseProtocol = Depends(get_create_lesson_group_student_use_case),
    access_token: str = Depends(access_token_schema)

):
    return await create(data, access_token)

@router.post("/lesson-groups", response_model=list[LessonGroupReadSchema])
async def bulk_create_groups_with_students(
    data: list[LessonGroupCreateSchema],
    bulk_create: BulkCreateLessonGroupStudentUseCaseProtocol = Depends(get_bulk_create_lesson_group_student_use_case),
    access_token: str = Depends(access_token_schema)
):
    return await bulk_create(data, access_token)