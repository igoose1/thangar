from typing import List, Tuple
from datetime import datetime

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from sqlalchemy.orm import Session

import crud, schemas
import config


def Client(session: StringSession):
    return TelegramClient(
        session, api_id=config.api_id, api_hash=config.api_hash
    )


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


def park(db: Session) -> schemas.AirplaneCreate:
    with Client(StringSession()) as client:
        client.start()
        return crud.build_airplane(db, airplane_from_client(client))


def soar(db: Session, id: int) -> List[Tuple[str, datetime]]:
    airplane = crud.airplane_by_id(db, id)
    with Client(StringSession(airplane.session)) as client:
        messages = client.get_messages(
            config.service_id, from_user=config.service_id, limit=10
        )
        result = [(m.text, m.date) for m in messages[:2]]
        return result
