from sqlalchemy import (
    Column,
    String,
    Integer,
)

from database import Base


class Airplane(Base):
    __tablename__ = "airplanes"

    id = Column(Integer, primary_key=True, index=True)
    session = Column(String, unique=True)
    user_name = Column(String)
