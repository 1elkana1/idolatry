from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

from app.db.db import SessionLocal
from app.db import mappers

db = SessionLocal()

# ---- import game logic ----
from app.core.entities import Entity
from app.core.deities import Deity

# ---- API models ----
class EntityCreate(BaseModel):
    name: str
    patron_id: int

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
    mappers.save_deity(db, d)
    return {"message": f"Deity {d.name} created."}

@app.post("/entity")
def create_entity(entity: EntityCreate):
    d = mappers.load_deity(db, entity.patron_id)
    e = Entity(entity.name, d)
    mappers.save_entity(db, e)
    return {"message": f"Entity {e.name} created."}

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