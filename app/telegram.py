from typing import List, Tuple
from datetime import datetime

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from sqlalchemy.orm import Session

import crud, schemas
import config


def park(db: Session) -> schemas.AirplaneCreate:
    with TelegramClient(
        StringSession(), config.api_id, config.api_hash
    ) as client:
        client.start()
        me = client.get_me()
        airplane = schemas.AirplaneCreate(
            id=me.id,
            user_name=(
                f"{me.first_name} {me.last_name}"
                if me.last_name
                else me.first_name
            ),
            session=client.session.save(),
        )
        return crud.build_airplane(db, airplane)


def soar(db: Session, id: int) -> List[Tuple[str, datetime]]:
    airplane = crud.airplane_by_id(db, id)
    with TelegramClient(
        StringSession(airplane.session), config.api_id, config.api_hash
    ) as client:
        messages = client.get_messages(config.service_id, limit=5)
        result = [(m.text, m.date) for m in messages]
        return result
