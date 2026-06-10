from sqlalchemy.orm import Session
from app.events.domain.entities import Event, EventZone, PricingTier
from app.events.schemas.request import EventCreate

def get_all_events(db: Session):
    return db.query(Event).all()

def create_event(db: Session, event_data: EventCreate):
    # Extraemos las zonas para manejarlas por separado
    zones_data = event_data.zones
    
    # Creamos el evento base
    # Filtramos 'zones' para que no explote al crear el modelo SQLAlchemy
    event_dict = event_data.model_dump(exclude={"zones"})
    db_event = Event(**event_dict)
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Si hay zonas (Creación avanzada)
    if zones_data:
        for zone_item in zones_data:
            tiers_data = zone_item.tiers
            
            # Crear Zona
            db_zone = EventZone(
                event_id=db_event.id,
                name=zone_item.name,
                total_capacity=zone_item.total_capacity,
                is_numbered=zone_item.is_numbered
            )
            db.add(db_zone)
            db.commit()
            db.refresh(db_zone)

            # Crear Tiers para esta zona
            if tiers_data:
                for tier_item in tiers_data:
                    db_tier = PricingTier(
                        zone_id=db_zone.id,
                        **tier_item.model_dump()
                    )
                    db.add(db_tier)
        
        db.commit()
        db.refresh(db_event)

    return db_event
