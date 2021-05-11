from pydantic import BaseModel


class AirplaneBase(BaseModel):
    session: str
    user_name: str
    id: int


class AirplaneCreate(AirplaneBase):
    pass


class Airplane(AirplaneBase):
    class Config:
        orm_mode = True
