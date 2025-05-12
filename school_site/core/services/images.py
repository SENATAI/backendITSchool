from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error
import asyncio
import io
from typing import Protocol
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class ImageServiceProtocol(Protocol):
    async def upload(self, path: str, image: UploadFile) -> bool:
        ...
    
    async def get_url(self, path: str) -> str:
         ...
    
    # async def get_product_images(self, product_id: int, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
    #     ...
    
    # async def get_all_images(self, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
    #     ...
        
    async def delete(self, image_id: str) -> bool:
         ...


class MinioImageService(ImageServiceProtocol):
    def __init__(self, minio_client: Minio, bucket_name: str):
        self.client = minio_client
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            raise Exception(f"Failed to create bucket: {e}")
        
    async def upload(self, path: str, image: UploadFile) -> bool:
        image_data = await image.read()
        await self._run_sync(
            self.client.put_object,
            self.bucket_name,
            path,
            io.BytesIO(image_data),
            len(image_data),
            image.content_type
        )
        return True
    

    async def get_url(self, path: str) -> str:
        original_url = await self._run_sync(
            self.client.presigned_get_object,
            self.bucket_name,
            path,
            timedelta(minutes=30)
        )
        
        new_url = original_url.replace("http://minio:9000", "http://localhost/minio")
        
        logger.info(f"URL: {new_url}")
        return new_url
        

    async def delete(self, path: str) -> bool:
        """
        Удаляет изображение из MinIO по image_id (пути)
        
        :param image_id: Путь к объекту в MinIO (например, "products/123/photo.jpg")
        :return: True если удален, False если объект не найден
        """
        try:
            await self._run_sync(
                self.client.stat_object,
                self.bucket_name,
                path
            )
            await self._run_sync(
                self.client.remove_object,
                self.bucket_name,
                path
            )
            return True
        except S3Error as e:
            if e.code == 'NoSuchKey':
                return False  
            raise  

    async def _run_sync(self, func, *args):
        """Обертка для выполнения синхронных MinIO-операций в executor'е"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, func, *args)