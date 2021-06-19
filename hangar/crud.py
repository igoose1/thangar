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

from typing import List

from . import models
from . import schemas
from sqlalchemy.orm import Session


def airplanes(db: Session) -> List[schemas.Airplane]:
    return db.query(models.Airplane).all()


def airplane_by_id(db: Session, id: int) -> schemas.Airplane:
    return db.query(models.Airplane).filter(models.Airplane.id == id).first()


def update_airplane_by_id(db: Session, id: int, airplane: schemas.Airplane):
    db.query(models.Airplane).filter(models.Airplane.id == id).update(
        airplane.dict()
    )


def build_airplane(
    db: Session, airplane: schemas.AirplaneCreate
) -> schemas.Airplane:
    db_airplane = models.Airplane(**airplane.dict())
    db.add(db_airplane)
    db.commit()
    db.refresh(db_airplane)
    return db_airplane


def destroy_airplane(db: Session, airplane: schemas.Airplane) -> None:
    db.query(models.Airplane).filter(models.Airplane.id == airplane.id).delete()
