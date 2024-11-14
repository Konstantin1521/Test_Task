import json
import logging

from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth import auth as utils_auth
from core.models import db_helper
from rabbitmq import broker, queue

from .image_schema import Image, ImageCreate, ImageUpdate
from ..users.user_schema import UserResponse
from ..crud.crud_user_and_image import CRUDImage
from  core.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


router = APIRouter(tags=["images"])


@router.get("/get_all", response_model=list[Image])
async def get_images(
    current_user: UserResponse = Depends(utils_auth.get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):

    try:
        images = await CRUDImage.get_all_elements(session=session)
        return images

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get images",
        )


@router.get("/get/{image_id}", response_model=Image)
async def get_image(
    image_id: Annotated[int, Path],
    current_user: UserResponse = Depends(utils_auth.get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    image = await CRUDImage.get_element_by_id(session=session, element_id=image_id)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return image


@router.post("/create/", response_model=ImageCreate)
async def create_image(
    image_create: ImageCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserResponse = Depends(utils_auth.get_current_auth_user),
):
    try:
        image = await CRUDImage.create_element(
            session=session, element_create=image_create
        )

        try:
            image_data = {
                "User_id": current_user.id,
                "Image_id": image.id,
                "Method": "create",
            }
            await broker.publish(json.dumps(image_data), queue=queue.name)
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")

        return image
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Create failed try again later",
        )


@router.put("/update/{image_id}", response_model=Image)
async def update_image(
    image_id: Annotated[int, Path],
    image_update: ImageUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserResponse = Depends(utils_auth.get_current_auth_user),
):
    try:
        image = await CRUDImage.get_element_by_id(session=session, element_id=image_id)
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
            )
        image = await CRUDImage.update_element(
            session=session, element=image, element_update=image_update
        )

        try:

            image_data = {
                "User_id": current_user.id,
                "Image_id": image.id,
                "Method": "update",
            }

            await broker.publish(json.dumps(image_data), queue=queue.name)

        except Exception as e:
            logger.error(f"Failed to publish message: {e}")

        return image
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update failed try again later",
        )


@router.delete(
    "/delete/{image_id}",
)
async def delete_image(
    image_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserResponse = Depends(utils_auth.get_current_auth_user),
):
    try:
        image = await CRUDImage.get_element_by_id(session=session, element_id=image_id)
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
            )
        await CRUDImage.delete_element(session=session, element=image)

        try:
            image_data = {
                "User_id": current_user.id,
                "Image_id": image.id,
                "Method": "delete",
            }

            await broker.publish(json.dumps(image_data), queue=queue.name)

        except Exception as e:
            logger.error(f"Failed to publish message: {e}")

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delete failed try again later",
        )

    return {"status": "success"}
