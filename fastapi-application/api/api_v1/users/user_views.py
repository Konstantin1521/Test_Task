from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .user_schema import UserCreate, UserResponse
from auth import utils_jwt as jwt_auth
from ..crud.crud_user_and_image import CRUDUser


router = APIRouter(tags=["users"])


@router.post("/register", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        if not user_create.username or not user_create.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data"
            )

        existing_user = await CRUDUser.get_element_by_name(
            session=session, element_name=user_create.username
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        hashed_password = jwt_auth.hash_password(password=user_create.password)
        user_create.password = hashed_password
        user = await CRUDUser.create_element(
            session=session, element_create=user_create
        )
        return UserResponse(
            id=user.id, username=user.username, created_at=user.created_at
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
