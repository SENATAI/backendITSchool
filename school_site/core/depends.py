from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .services.images import ImageServiceProtocol, MinioImageService
from .clients.minio import get_minio_client

def get_image_service(bucket_name: str) -> ImageServiceProtocol:
    """Глобальная зависимость для получения сервиса изображений."""
    client = get_minio_client() 
    return MinioImageService(client, bucket_name)

def get_scheduler() -> AsyncIOScheduler:
    return AsyncIOScheduler()