from sqlalchemy import Column, String, DateTime, Float, func
from .base import Base


class Image(Base):

    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_date = Column(DateTime, default=func.now(), nullable=False)
    resolution = Column(String, nullable=False)
    size = Column(Float, nullable=False)
