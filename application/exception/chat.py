from fastapi import status

from application.exception.base import BaseAPIException


class ChatBadRequest(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Пользователь пытается создать чат с самим собой"
