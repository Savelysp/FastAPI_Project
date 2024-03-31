from fastapi import APIRouter

from api.handlers.v1 import service


router = APIRouter(prefix="/v1")
router.include_router(router=service.router)
