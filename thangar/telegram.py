# Copyright 2021 Oskar Sharipov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime

import telegram
from sqlalchemy.orm import Session
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from . import config, crud, schemas


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


def soar(
    db: Session, id: int, api: API
) -> typing.List[typing.Tuple[str, datetime]]:
    airplane = crud.airplane_by_id(db, id)
    with Client(StringSession(airplane.session), api) as client:
        messages = client.get_messages(
            config.service_id, from_user=config.service_id, limit=10
        )
        result = [(m.text, m.date) for m in messages[:2]]
        return result
