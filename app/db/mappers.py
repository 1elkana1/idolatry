from app.core.entities import Entity
from app.core.deities import Deity
from app.core.cults import Cult
from app.db.models import EntityDB, DeityDB, CultDB
from sqlalchemy.orm import Session

# ---- DB → Core ----
def load_entity(db: Session, entity_id) -> Entity | None:
    db_entity = db.get(EntityDB, entity_id)
    if db_entity:
        return Entity(
            name=db_entity.name,
            army=db_entity.army, # type: ignore
            wealth=db_entity.wealth, # type: ignore
            id=db_entity.id
            # cults will be hydrated separately if needed
        )

def load_deity(db: Session, deity_id) -> Deity | None:
    db_deity = db.get(DeityDB, deity_id)
    if db_deity:
        return Deity(
            name=db_deity.name,
            domain=db_deity.domain,
            id=db_deity.id
            # cults will be hydrated separately if needed
        )
    
def hydrate_entity_cults(db: Session, entity: Entity):
    db_cults = db.query(CultDB).filter(CultDB.entity_id == entity.id).all()
    for db_cult in db_cults:
        deity = load_deity(db, db_cult.deity_id)
        cult = Cult(entity, deity)
        cult.offerings = db_cult.offerings

def hydrate_deity_cults(db: Session, deity: Deity):
    db_cults = db.query(CultDB).filter(CultDB.deity_id == deity.id).all()
    for db_cult in db_cults:
        entity = load_entity(db, db_cult.entity_id)
        cult = Cult(entity, deity)
        cult.offerings = db_cult.offerings

def load_cult(db: Session, cult_id) -> Cult | None:
    db_cult = db.get(CultDB, cult_id)
    if db_cult:
        entity = load_entity(db, db_cult.entity_id)
        deity = load_deity(db, db_cult.deity_id)
        cult = Cult(entity, deity, db_cult.id)
        cult.offerings = db_cult.offerings
        return cult
    return None

# ---- Core → DB ----
def save_entity(db: Session, entity: Entity):
    if entity.id:
        db_entity = db.get(EntityDB, entity.id)
        if not db_entity:
            raise ValueError("Entity not found in DB")
    else:
        db_entity = EntityDB(name=entity.name)
        db.add(db_entity)
    db_entity.army = entity.army # type: ignore
    db_entity.wealth = entity.wealth # type: ignore
    db.commit()
    db.refresh(db_entity)
    entity.id = db_entity.id
    return entity.id

def save_deity(db: Session, deity: Deity):
    if deity.id:
        db_deity = db.get(DeityDB, deity.id)
        if not db_deity:
            raise ValueError("Deity not found in DB")
    else:
        db_deity = DeityDB(
            name=deity.name,
            domain=deity.domain
        )
        db.add(db_deity)
    db.commit()
    db.refresh(db_deity)
    deity.id = db_deity.id
    return deity.id

def save_cult(db: Session, cult: Cult):
    if not cult.entity.id or not cult.deity.id:
        raise ValueError("Both Entity and Deity must be saved before saving Cult")
    if cult.id:
        db_cult = db.get(CultDB, cult.id)
        if not db_cult:
            raise ValueError("Cult not found in DB")
    else:
        db_cult = CultDB(
            entity_id=cult.entity.id,
            deity_id=cult.deity.id,
        )
    db_cult.offerings = cult.offerings # type: ignore
    db.commit()
    db.refresh(db_cult)
    cult.id = db_cult.id
    return cult.id
