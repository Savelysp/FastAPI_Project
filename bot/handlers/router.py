from fastapi import APIRouter

from bot.handlers import v1


bot_router = APIRouter(prefix="/bot")
bot_router.include_router(router=v1.router)
