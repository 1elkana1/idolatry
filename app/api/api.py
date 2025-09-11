from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

from app.db.db import SessionLocal
from app.db import mappers

db = SessionLocal()

from app.core.entities import Entity
from app.core.deities import Deity
from app.db.repositories.entities_repo import EntityRepository
from app.db.repositories.deities_repo import DeityRepository
from app.db.repositories.cults_repo import CultRepository

# ---- api models ----
class EntityCreate(BaseModel):
    name: str
    patron_id: Optional[int] = None

class DeityCreate(BaseModel):
    name: str
    domain: str

class Offering(BaseModel):
    entity_id: int
    deity_id: int
    amount: int

class Battle(BaseModel):
    attacker_id: int
    defender_id: int


# ---- API endpoints ----

@app.post("/deity")
def create_deity(deity: DeityCreate):
    d = Deity(deity.name, deity.domain)
    deities_repo = DeityRepository(db)
    deities_repo.save_without_cults(d)
    db.commit()
    # mappers.save_deity(db, d)
    return {"message": f"Deity {d.name} created."}

@app.get("/deity/{deity_id}")
def get_deity(deity_id: int):
    deities_repo = DeityRepository(db)
    deity = deities_repo.get_without_cults(deity_id)
    if not deity:
        return {"error": "Deity not found"}
    deities_repo.populate_deity_cults(deity, EntityRepository(db), CultRepository(db))
    return {
        "id": deity.id,
        "name": deity.name,
        "domain": deity.domain,
        "cults": [
            {
                "entity_id": cult.entity.id,
                "entity_name": cult.entity.name,
                "offerings": cult.offerings
            } for cult in deity.cults
        ]
    }    

@app.post("/entity")
def create_entity(entity: EntityCreate):
    entities_repo = EntityRepository(db)
    e = Entity(entity.name)
    entities_repo.save_without_cults(e)
    if entity.patron_id:
        deities_repo = DeityRepository(db)
        patron = deities_repo.get_without_cults(entity.patron_id)
        if not patron:
            return {"error": "Patron Deity not found"}
        e.establish_cult_to(patron)
        entities_repo.save_entity_cults(e, CultRepository(db), deities_repo)
    db.commit()
    # d = mappers.load_deity(db, entity.patron_id)
    # e = Entity(entity.name, d)
    # mappers.save_entity(db, e)
    return {"message": f"Entity {e.name} created."}

@app.get("/entity/{entity_id}")
def get_entity(entity_id: int):
    entities_repo = EntityRepository(db)
    entity = entities_repo.get_without_cults(entity_id)
    if not entity:
        return {"error": "Entity not found"}
    entities_repo.populate_entity_cults(entity, DeityRepository(db), CultRepository(db))
    return {
        "id": entity.id,
        "name": entity.name,
        "army": entity.army,
        "wealth": entity.wealth,
        "cults": [
            {
                "deity_id": cult.deity.id,
                "deity_name": cult.deity.name,
                "offerings": cult.offerings
            } for cult in entity.cults
        ]
    }

@app.post("/battle")
def initiate_battle(battle: Battle):
    attacker = mappers.load_entity(db, battle.attacker_id)
    defender = mappers.load_entity(db, battle.defender_id)
    if not attacker or not defender:
        return {"error": "Invalid attacker or defender"}
    attacker.attack(defender)
    mappers.save_entity(db, attacker)
    mappers.save_entity(db, defender)
    return {"message": f"Battle between {attacker.name} and {defender.name} concluded."}

@app.post("/offering")
def make_offering(offering: Offering):
    entity = mappers.load_entity(db, offering.entity_id)
    deity = mappers.load_deity(db, offering.deity_id)
    if not entity or not deity:
        return {"error": "Invalid entity or deity"}
    entity.offer_to(deity, offering.amount)
    mappers.save_entity(db, entity)
    mappers.save_deity(db, deity)
    mappers.save_cult(db, entity.cults[0])
    return {"message": f"{entity.name} offered {offering.amount} to {deity.name}. full offerings: {entity.cults[0].offerings}."}

@app.get("/state")
def game_state():
    entity = mappers.load_entity(db, 1)
    deity = mappers.load_deity(db, 1)
    if entity and deity:
        return {
            "entities": entity.name,
            "deities": deity.name
        }