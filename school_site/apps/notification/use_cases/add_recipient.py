from typing import Protocol, Self

from school_site.apps.notification.schemas import (
    NotificationRecipientCreateSchema,
    NotificationRecipientReadSchema
)
from school_site.apps.notification.services.notification import NotificationServiceProtocol


class AddRecipientUseCaseProtocol(Protocol):
    async def execute(
        self: Self,
        recipient_data: NotificationRecipientCreateSchema
    ) -> NotificationRecipientReadSchema:
        ...


class AddRecipientUseCase(AddRecipientUseCaseProtocol):
    def __init__(self: Self, notification_service: NotificationServiceProtocol):
        self.notification_service = notification_service

    async def execute(
        self: Self,
        recipient_data: NotificationRecipientCreateSchema
    ) -> NotificationRecipientReadSchema:
        return await self.notification_service.add_recipient(recipient_data)