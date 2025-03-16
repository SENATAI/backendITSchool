"""
Основной модуль для роутов приложения.
"""

from fastapi import FastAPI

from school_site.apps.users.router import router as users_router
from school_site.apps.products.router import router as product_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Применяем роуты приложения.
    """

    app.include_router(users_router)
    app.include_router(product_router)
    return app