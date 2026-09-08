from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/auth")
def auth_credentials():
    pass
