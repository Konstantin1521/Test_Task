from typing import Type, TypeVar, Generic, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from core.models import Image, User

ModelType = TypeVar("ModelType")


class CRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get_all_elements(self, session: AsyncSession) -> Sequence[ModelType]:
        try:
            stmt = select(self.model).order_by(self.model.id)
            result: Result = await session.execute(stmt)
            elements = result.scalars().all()
            return elements
        except Exception as e:
            raise Exception(f"Failed to get elements: {e}")

    async def get_element_by_id(
        self, session: AsyncSession, element_id: int
    ) -> ModelType | None:
        try:
            stmt = select(self.model).where(self.model.id == element_id)
            result: Result = await session.execute(stmt)
            elm = result.scalar()
            return elm
        except Exception as e:
            raise Exception(f"Failed to get element: {e}")

    async def get_element_by_name(
        self, session: AsyncSession, element_name: str
    ) -> ModelType | None:
        try:
            stmt = select(self.model).where(self.model.username == element_name)
            result: Result = await session.execute(stmt)
            elm = result.scalar()
            return elm
        except Exception:
            return None


    async def create_element(
        self, session: AsyncSession, element_create: ModelType
    ) -> ModelType:
        try:
            element = self.model(**element_create.model_dump())
            session.add(element)
            await session.commit()
            await session.refresh(element)
            return element
        except Exception as e:
            raise Exception(f"Failed to create element: {e}")

    async def update_element(
        self, session: AsyncSession, element: ModelType, element_update: ModelType
    ) -> ModelType | None:
        try:
            for attr, value in element_update.model_dump(exclude_unset=True).items():
                setattr(element, attr, value)
            await session.commit()
            await session.refresh(element)
            return element
        except Exception as e:

            raise Exception(f"Failed to update element: {e}")

    async def delete_element(self, session: AsyncSession, element: ModelType) -> None:
        await session.delete(element)
        await session.commit()


CRUDImage = CRUD(Image)
CRUDUser = CRUD(User)
