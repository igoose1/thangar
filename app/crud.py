from typing import List

from sqlalchemy.orm import Session

import models, schemas


def airplanes(db: Session) -> List[schemas.Airplane]:
    return db.query(models.Airplane).all()


def airplane_by_id(db: Session, id: int) -> schemas.Airplane:
    return db.query(models.Airplane).filter(models.Airplane.id == id).first()


def build_airplane(
    db: Session, airplane: schemas.AirplaneCreate
) -> models.Airplane:
    db_airplane = models.Airplane(
        session=airplane.session,
        id=airplane.id,
        user_name=airplane.user_name,
    )
    db.add(db_airplane)
    db.commit()
    db.refresh(db_airplane)
    return db_airplane


def destroy_airplane(db: Session, airplane: schemas.Airplane) -> None:
    db.query(models.Airplane).filter(models.Airplane.id == airplane.id).delete()
