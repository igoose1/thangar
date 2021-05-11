from datetime import datetime
from typing import List, Tuple

import config
import crud
import schemas
from sqlalchemy.orm import Session
from telethon.sessions import StringSession
from telethon.sync import TelegramClient


class API:
    def __init__(self, id: int, hash: str):
        self.id = id
        self.hash = hash


def Client(session: StringSession, api: API):
    return TelegramClient(session, api_id=api.id, api_hash=api.hash)


def airplane_from_client(client: TelegramClient) -> schemas.AirplaneCreate:
    me = client.get_me()
    airplane = schemas.AirplaneCreate(
        session=client.session.save(),
        id=me.id,
        name=(
            f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
        ),
        phone=me.phone,
        username=me.username,
    )
    return airplane


def park(db: Session, api: API) -> schemas.AirplaneCreate:
    with Client(StringSession(), api) as client:
        client.start()
        return crud.build_airplane(db, airplane_from_client(client))


def repark(db: Session, api: API) -> None:
    for airplane in crud.airplanes(db):
        with Client(StringSession(airplane.session), api) as client:
            new_airplane = airplane_from_client(client)
            crud.update_airplane_by_id(db, airplane.id, new_airplane)


def soar(db: Session, id: int, api: API) -> List[Tuple[str, datetime]]:
    airplane = crud.airplane_by_id(db, id)
    with Client(StringSession(airplane.session), api) as client:
        messages = client.get_messages(
            config.service_id, from_user=config.service_id, limit=10
        )
        result = [(m.text, m.date) for m in messages[:2]]
        return result
