"""Persons API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..dependencies import get_db
from ...database.models import Person
from ..schemas.person import PersonCreate, PersonRead

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("", response_model=List[PersonRead])
def list_persons(db: Session = Depends(get_db)):
    persons = db.query(Person).order_by(Person.name.asc()).all()
    return persons


@router.post("", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_person(payload: PersonCreate, db: Session = Depends(get_db)):
    # Check uniqueness
    existing = db.query(Person).filter(Person.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Person with this name already exists")

    person = Person(name=payload.name, is_active=payload.is_active)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

