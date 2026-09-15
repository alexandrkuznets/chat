

class BaseAPIException(Exception):
    status_code: int
    message: str