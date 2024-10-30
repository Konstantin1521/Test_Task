from fastapi import APIRouter

from .api_v1.image.image_views import router as image_router
from .api_v1.users.user_views import router as user_router
from auth.auth import router as auth_router

api_router = APIRouter()
api_router.include_router(image_router)
api_router.include_router(user_router)
api_router.include_router(auth_router)
