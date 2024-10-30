from sqlalchemy import (
    Column,
    String,
    DateTime,
    LargeBinary,
    func
    )


from .base import Base


class User(Base):
    username = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
