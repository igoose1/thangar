from pydantic import BaseModel


class AirplaneBase(BaseModel):
    session: str
    id: int
    name: str
    phone: str
    username: str


class AirplaneCreate(AirplaneBase):
    pass


class Airplane(AirplaneBase):
    class Config:
        orm_mode = True
