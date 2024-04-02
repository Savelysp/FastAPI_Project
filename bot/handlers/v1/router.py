from fastapi import APIRouter

from api.handlers.v1 import echo


router = APIRouter(prefix="/v1")
router.include_router(router=echo.router)
