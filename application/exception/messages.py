from exception.base import BaseAPIException
from fastapi import status


class ConversationNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Собеседник не найден"