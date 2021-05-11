from sqlalchemy import (
    Column,
    String,
    Integer,
)

from database import Base


class Airplane(Base):
    __tablename__ = "airplanes"

    session = Column(String, unique=True, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
