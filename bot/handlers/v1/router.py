from fastapi import APIRouter

from bot.handlers.v1 import echo


router = APIRouter(prefix="/v1")
router.include_router(router=echo.router)
