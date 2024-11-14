from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class ImageSchema(BaseModel):
    title: str
    file_path: str
    resolution: str
    size: float


class ImageCreate(ImageSchema):
    pass


class ImageUpdate(ImageCreate):

    title: str | None = None
    file_path: str | None = None
    resolution: str | None = "800x600"
    size: float | None = 1024


class Image(ImageSchema):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    upload_date: datetime

