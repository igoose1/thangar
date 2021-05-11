from typing import List

from sqlalchemy.orm import Session

import models, schemas


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
