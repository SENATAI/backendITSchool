from fastapi import APIRouter, Depends, Cookie, Path, UploadFile, File, Form, Query
import json
from uuid import UUID
from typing import Optional
from .use_cases.create_product import CreateProductUseCaseProtocol
from .use_cases.update_product import UpdateProductUseCaseProtocol
from .use_cases.get_product import GetProductUseCaseProtocol
from .use_cases.delete_product import DeleteProductUseCaseProtocol
from .use_cases.list_product import GetListProductUseCaseProtocol
from .depends import (
    get_product_create_use_case, get_product_update_use_case, get_product_get_use_case,
    get_product_delete_use_case, get_product_get_list_use_case
) 
from .schemas import ProductReadSchema, ProductCursorPaginationResultSchema

router = APIRouter(prefix='/api/products', tags=['Products'])

@router.post("/", response_model=ProductReadSchema)
async def create_product(
    product_data: str = Form(...),
    access_token: str = Cookie(...),
    image: Optional[UploadFile] = File(None),
    create: CreateProductUseCaseProtocol = Depends(get_product_create_use_case)
):
    created_product = await create(access_token, product_data, image)
    return created_product


@router.put("/{product_id}", response_model=ProductReadSchema)
async def update_product(
    product_data: str = Form(...),
    product_id: UUID = Path(...),
    access_token: str = Cookie(...),
    image: Optional[UploadFile] = File(None),
    update: UpdateProductUseCaseProtocol = Depends(get_product_update_use_case)
):
    updated_product = await update(access_token, product_id, product_data, image)
    return updated_product

@router.get("/{product_id}", response_model=ProductReadSchema)
async def get_product(
    product_id: UUID = Path(...),
    get: GetProductUseCaseProtocol = Depends(get_product_get_use_case)
):
    product = await get(product_id)
    return product

@router.get("/", response_model=ProductCursorPaginationResultSchema)
async def list_products(
    search: Optional[str] = Query(None),
    search_by: Optional[list[str]] = Query(None),
    cursor: Optional[UUID] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    list: GetListProductUseCaseProtocol = Depends(get_product_get_list_use_case)
):
    products = await list(search, search_by, cursor, limit)
    return products
    

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: UUID = Path(...),
    access_token: str = Cookie(...),
    delete: DeleteProductUseCaseProtocol = Depends(get_product_delete_use_case)
):
    await delete(access_token, product_id)

    return None


