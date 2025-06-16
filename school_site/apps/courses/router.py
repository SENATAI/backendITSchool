from fastapi import APIRouter, Depends, Path, Query, UploadFile, File, Form
from school_site.apps.users.depends import access_token_schema
from uuid import UUID
from typing import Optional, Union
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
from .use_cases.lesson_group_student.create_lesson_group_student import CreateLessonGroupStudentUseCaseProtocol
from .use_cases.lesson_group_student.bulk_create_lesson_group_student import BulkCreateLessonGroupStudentUseCaseProtocol
from .use_cases.add_homework import AddHomeworkUseCaseProtocol
from .use_cases.comments.create_comment import CreateCommentUseCaseProtocol
from .use_cases.comments.update_comment import UpdateCommentUseCaseProtocol
from .use_cases.comments.delete_comment import DeleteCommentUseCaseProtocol
from .use_cases.lesson_group.update_lesson_group import UpdateLessonGroupUseCaseProtocol
from .use_cases.lessons.get_teacher_lesson_with_materials import GetTeacherMaterialUseCaseProtocol
from .use_cases.lessons.get_student_lesson_with_material import GetStudentMaterialUseCaseProtocol
from .use_cases.lessons.get_lesson_info_teacher import GetTeacherLessonInfoUseCaseProtocol
from .use_cases.courses_students.get_courses_for_student import GetCoursesForStudentUseCaseProtocol
from .use_cases.courses_teachers.get_courses_for_teacher import GetCoursesForTeacherUseCaseProtocol
from .use_cases.lesson_group.get_by_group_id import GetByGroupIdLessonGroupUseCaseProtocol 
from .depends import (
    get_course_create_use_case, get_course_update_use_case, get_course_get_use_case,
    get_course_delete_use_case, get_course_get_list_use_case,
    get_lesson_create_use_case, get_lesson_update_use_case, get_lesson_get_use_case,
    get_lesson_delete_use_case, get_lesson_get_list_use_case, get_material_create_use_case,
    get_material_update_use_case, get_material_get_use_case, get_material_delete_use_case,
    get_create_lesson_group_student_use_case, get_bulk_create_lesson_group_student_use_case,
    get_add_homework_use_case, get_teacher_lesson_info_use_case,
    get_create_comment_use_case, get_update_comment_use_case, get_delete_comment_use_case,
    get_lesson_group_update_use_case, get_lesson_for_teacher_use_case, get_lesson_for_student_use_case,
    get_courses_for_student_use_case, get_courses_for_teacher_use_case, 
    get_by_group_id_lesson_group_use_case
)
from .schemas import (
    CourseWithPhotoReadSchema, CourseWithPhotoPaginationResultSchema,
    LessonReadSchema, LessonPaginationResultSchema, LessonCreateSchema, LessonUpdateSchema,
    LessonWithMaterialsCreateSchema, LessonWithMaterialsUpdateSchema, LessonHTMLCreateSchema, 
    LessonHTMLUpdateSchema, LessonWithMaterialsReadSchema, LessonWithMaterialsDeleteSchema,
    LessonGroupReadSchema, LessonGroupCreateSchema, LessonGroupUpdateSchema, LessonHTMLReadSchema, AddHomeworkReadSchema,
    CommentCreateSchema, CommentReadSchema, CommentUpdateSchema, LessonSimpleReadSchema, LessonStudentMaterialDetailReadSchema,
    LessonTeacherMaterialDetailReadSchema, LessonInfoTeacherReadSchema, CourseStudentWithCoursesSchema,
    LessonGroupReadWithLessonSchema
)

router = APIRouter(prefix='/api/courses', tags=['Courses'])

@router.get("/student", response_model=list[CourseStudentWithCoursesSchema], status_code=200)
async def get_courses_for_student(
    access_token: str = Depends(access_token_schema),
    get_courses_for_student: GetCoursesForStudentUseCaseProtocol = Depends(get_courses_for_student_use_case)
):
    return await get_courses_for_student(access_token)

@router.get("/teacher", response_model=list[CourseWithPhotoReadSchema], status_code=200)
async def get_courses_for_teacher(
    access_token: str = Depends(access_token_schema),
    get_courses_for_teacher: GetCoursesForTeacherUseCaseProtocol = Depends(get_courses_for_teacher_use_case)
):
    return await get_courses_for_teacher(access_token)

@router.post("/lesson-group", response_model=LessonGroupReadSchema)
async def create_group_with_students(
    data: LessonGroupCreateSchema,
    create: CreateLessonGroupStudentUseCaseProtocol = Depends(get_create_lesson_group_student_use_case),
    access_token: str = Depends(access_token_schema)

):
    return await create(data, access_token)

@router.get("/lesson-group", response_model=list[LessonGroupReadWithLessonSchema])
async def get_lesson_group_by_id(
    group_id: UUID = Query(...),
    get: GetByGroupIdLessonGroupUseCaseProtocol = Depends(get_by_group_id_lesson_group_use_case),
    access_token: str = Depends(access_token_schema)

):
    return await get(group_id)

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
    teacher_material_id, teacher_material_url = await _create_material_if_exists(
        data.teacher_material_name, data.teacher_material_text, material_create_use_case, access_token
    )
    student_material_id, student_material_url = await _create_material_if_exists(
        data.student_material_name, data.student_material_text, material_create_use_case, access_token
    )
    homework_id, homework_url = await _create_material_if_exists(
        data.homework_material_name, data.homework_material_text, material_create_use_case, access_token
    )

    lesson = LessonCreateSchema(
        name=data.name,
        teacher_material_id=teacher_material_id,
        student_material_id=student_material_id,
        homework_id=homework_id
    )
    
    created_lesson = await lesson_create_use_case(course_id, lesson, access_token)
    
    return LessonWithMaterialsReadSchema(
        id=created_lesson.id,
        course_id=created_lesson.course_id,
        name=created_lesson.name,
        teacher_material_id=teacher_material_id,
        student_material_id=student_material_id,
        homework_id=homework_id,
        teacher_material_url=teacher_material_url,
        student_material_url=student_material_url,
        homework_material_url=homework_url
    )

async def _create_material_if_exists(
    name: Optional[str],
    text: Optional[str],
    material_use_case: CreateLessonHTMLFileUseCaseProtocol,
    access_token: str
):
    if name and text:
        material = LessonHTMLCreateSchema(name=name, html_text=text)
        created = await material_use_case(material, access_token)
        return created.id, created.url
    return None, None


@router.put("/{course_id}/lessons-with-materials/{lesson_id}", response_model=LessonWithMaterialsReadSchema, status_code=200)
async def update_lesson_with_materials(
    data: LessonWithMaterialsUpdateSchema,
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    lesson_update_use_case: UpdateLessonUseCaseProtocol = Depends(get_lesson_update_use_case),
    material_update_use_case: UpdateLessonHTMLFileUseCaseProtocol = Depends(get_material_update_use_case),
    access_token: str = Depends(access_token_schema)
):
    updated_teacher_material = await _update_material_if_exists(
        data.teacher_material_id, data.teacher_material_name, data.teacher_material_text, material_update_use_case, access_token
    )
    updated_student_material = await _update_material_if_exists(
        data.student_material_id, data.student_material_name, data.student_material_text, material_update_use_case, access_token
    )
    updated_homework_material = await _update_material_if_exists(
        data.homework_material_id, data.homework_material_name, data.homework_material_text, material_update_use_case, access_token
    )

    lesson = LessonUpdateSchema(
        name=data.name,
        teacher_material_id=updated_teacher_material.id if updated_teacher_material else data.teacher_material_id,
        student_material_id=updated_student_material.id if updated_student_material else data.student_material_id,
        homework_id=updated_homework_material.id if updated_homework_material else data.homework_material_id
    )
    
    updated_lesson = await lesson_update_use_case(course_id, lesson_id, lesson, access_token)
    
    return LessonWithMaterialsReadSchema(
        id=updated_lesson.id,
        course_id=updated_lesson.course_id,
        name=updated_lesson.name,
        teacher_material_id=updated_teacher_material.id if updated_teacher_material else data.teacher_material_id,
        student_material_id=updated_student_material.id if updated_student_material else data.student_material_id,
        homework_id=updated_homework_material.id if updated_homework_material else data.homework_material_id,
        teacher_material_url=updated_teacher_material.url if updated_teacher_material else None,
        student_material_url=updated_student_material.url if updated_student_material else None,
        homework_material_url=updated_homework_material.url if updated_homework_material else None
    )


async def _update_material_if_exists(
    material_id: Optional[UUID],
    name: Optional[str],
    text: Optional[str],
    material_use_case: UpdateLessonHTMLFileUseCaseProtocol,
    access_token: str
):
    if material_id and name and text:
        material = LessonHTMLUpdateSchema(name=name, html_text=text)
        return await material_use_case(material_id, material, access_token)
    return None

@router.get("/{course_id}/lessons-with-materials/{lesson_id}", response_model=LessonWithMaterialsReadSchema, status_code=200)
async def get_lesson_with_materials(
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    get_lesson: GetLessonUseCaseProtocol = Depends(get_lesson_get_use_case),
    get_material: GetLessonHTMLFileUseCaseProtocol = Depends(get_material_get_use_case),
    access_token: str = Depends(access_token_schema)
):
    lesson = await get_lesson(course_id, lesson_id)
    teacher_material = await _get_material_if_exists(lesson.teacher_material_id, get_material, access_token)
    student_material = await _get_material_if_exists(lesson.student_material_id, get_material, access_token)
    homework_material = await _get_material_if_exists(lesson.homework_id, get_material, access_token)
    
    return LessonWithMaterialsReadSchema(
        id=lesson.id,
        course_id=lesson.course_id,
        name=lesson.name,
        teacher_material_id=teacher_material.id if teacher_material else None,
        student_material_id=student_material.id if student_material else None,
        homework_id=homework_material.id if homework_material else None,
        teacher_material_url=teacher_material.url if teacher_material else None,
        student_material_url=student_material.url if student_material else None,
        homework_material_url=homework_material.url if homework_material else None
    )


async def _get_material_if_exists(
    material_id: Optional[UUID],
    get_material_use_case: GetLessonHTMLFileUseCaseProtocol,
    access_token: str
):
    if material_id:
        return await get_material_use_case(material_id, access_token)
    return None


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
    if data.teacher_material_id:
        await delete_material(data.teacher_material_id, access_token)
    if data.student_material_id:
        await delete_material(data.student_material_id, access_token)
    if data.homework_material_id:
        await delete_material(data.homework_material_id, access_token)

    return None


@router.put("/lesson-group/{lesson_group_id}", response_model=LessonGroupReadSchema)
async def update_lesson_group(
    lesson_group: LessonGroupUpdateSchema,
    lesson_group_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    update: UpdateLessonGroupUseCaseProtocol = Depends(get_lesson_group_update_use_case)
):
    return await update(lesson_group_id, lesson_group, access_token)

@router.post("/lesson-groups", response_model=list[LessonGroupReadSchema])
async def bulk_create_groups_with_students(
    data: list[LessonGroupCreateSchema],
    bulk_create: BulkCreateLessonGroupStudentUseCaseProtocol = Depends(get_bulk_create_lesson_group_student_use_case),
    access_token: str = Depends(access_token_schema)
):
    return await bulk_create(data, access_token)

@router.post("/material", response_model=LessonHTMLReadSchema)
async def create_material(material: LessonHTMLCreateSchema,
                          access_token_schema: str = Depends(access_token_schema),
                        material_create_use_case: CreateLessonHTMLFileUseCaseProtocol = Depends(get_material_create_use_case)
                          ):
    return await material_create_use_case(material, access_token_schema)


@router.delete("/material/{material_id}", status_code=204)
async def delete_material(material_id: UUID = Path(...),
                          access_token_schema: str = Depends(access_token_schema),
                        delete_material: DeleteLessonHTMLFileUseCaseProtocol = Depends(get_material_delete_use_case)
                          ):
    return await delete_material(material_id, access_token_schema)


@router.put("/material/{material_id}")
async def update_material(
                        material: LessonHTMLUpdateSchema,
                        material_id: UUID = Path(...),
                        access_token_schema: str = Depends(access_token_schema),
                        update_material: UpdateLessonHTMLFileUseCaseProtocol = Depends(get_material_update_use_case)
                          ):
    return await update_material(material_id, material, access_token_schema)

@router.get("/material/{material_id}")
async def get_material(
    material_id: UUID = Path(...),
    access_token_schema: str = Depends(access_token_schema),
    get_material: GetLessonHTMLFileUseCaseProtocol = Depends(get_material_get_use_case)
):
    return await get_material(material_id, access_token_schema)
    

@router.post("/{course_id}/lessons/{lesson_id}/homework", response_model=AddHomeworkReadSchema, status_code=201)
async def create_homework(
    homework_data: str = Form(...),
    homework_file: Optional[UploadFile] = File(...),
    lesson_id: UUID = Path(...),
    access_token_schema: str = Depends(access_token_schema),
    add_homework: AddHomeworkUseCaseProtocol = Depends(get_add_homework_use_case)
):
    return await add_homework(lesson_id, homework_data, homework_file, access_token_schema)


@router.post("/{course_id}/lessons/{lesson_id}/comments", response_model=CommentReadSchema, status_code=201)
async def create_comment(
    comment: CommentCreateSchema,
    access_token_schema: str = Depends(access_token_schema),
    create_comment: CreateCommentUseCaseProtocol = Depends(get_create_comment_use_case)
):
    return await create_comment(comment, access_token_schema)

@router.put("/{course_id}/lessons/{lesson_id}/comments/{comment_id}", response_model=CommentReadSchema, status_code=200)
async def update_comment(
    comment: CommentUpdateSchema,
    comment_id: UUID = Path(...),
    access_token_schema: str = Depends(access_token_schema),
    update_comment: UpdateCommentUseCaseProtocol = Depends(get_update_comment_use_case)
):
    return await update_comment(comment_id, comment, access_token_schema)

@router.delete("/{course_id}/lessons/{lesson_id}/comments/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: UUID = Path(...),
    access_token_schema: str = Depends(access_token_schema),
    delete_comment: DeleteCommentUseCaseProtocol = Depends(get_delete_comment_use_case)
):
    await delete_comment(comment_id, access_token_schema)
    return None

@router.get("/{course_id}/lessons/{lesson_id}/student-materials", response_model=Union[LessonSimpleReadSchema, LessonStudentMaterialDetailReadSchema], status_code=200)
async def get_lesson_materials_for_student(
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    get_lesson_with_materials: GetStudentMaterialUseCaseProtocol = Depends(get_lesson_for_student_use_case)
):
    return await get_lesson_with_materials(lesson_id, access_token)

@router.get("/{course_id}/lessons/{lesson_id}/teacher-materials", response_model=Union[LessonSimpleReadSchema, LessonTeacherMaterialDetailReadSchema], status_code=200)
async def get_lesson_materials_for_teacher(
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    student_id: UUID = Query(...),
    access_token: str = Depends(access_token_schema),
    get_lesson_with_materials: GetTeacherMaterialUseCaseProtocol = Depends(get_lesson_for_teacher_use_case)
):
    return await get_lesson_with_materials(lesson_id, student_id, access_token)

@router.get("/{course_id}/lessons/{lesson_id}/teacher-info", response_model=LessonInfoTeacherReadSchema, status_code=200)
async def get_lesson_info_for_teacher(
    course_id: UUID = Path(...),
    lesson_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    get_lesson_info: GetTeacherLessonInfoUseCaseProtocol = Depends(get_teacher_lesson_info_use_case)
):
    return await get_lesson_info(lesson_id, access_token)

