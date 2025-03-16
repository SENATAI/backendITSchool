from fastapi import APIRouter, Depends, Cookie
from .use_cases.create_product import CreateProductUseCaseProtocol
from .depends import get_product_create_use_case
from .schemas import ProductReadSchema, ProductCreateSchema

router = APIRouter(prefix='/api/products', tags=['Products'])

@router.post("/", response_model=ProductReadSchema)
async def create(
    product: ProductCreateSchema,
    access_token: str = Cookie(...),
    create: CreateProductUseCaseProtocol = Depends(get_product_create_use_case)
):
    created_product = await create(access_token, product)
    return created_product