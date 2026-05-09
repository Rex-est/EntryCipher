from sqlalchemy.orm import Session
from app.events.domain.entities import Event
from app.events.schemas.request import EventCreate

def get_all_events(db: Session):
    return db.query(Event).all()

def create_event(db: Session, event: EventCreate):
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event