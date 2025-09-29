from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://1elkana1.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from db.db import SessionLocal

db = SessionLocal()

from core.entities import Entity
from core.deities import Deity
from db.repositories.entities_repo import EntityRepository
from db.repositories.deities_repo import DeityRepository
from db.repositories.cults_repo import CultRepository
from api.DTOs.schemas import EntitySchema, DeitySchema, CultSchema
from api.DTOs import serializers

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
    return {"message": f"Deity {d.id}.{d.name} created."}

@app.get("/deity/{deity_id}", response_model=DeitySchema)
def get_deity(deity_id: int):
    deities_repo = DeityRepository(db)
    deity = deities_repo.get_without_cults(deity_id)
    if not deity:
        raise HTTPException(status_code=404, detail=f"Deity {deity_id} not found")
    deities_repo.populate_deity_cults(deity, EntityRepository(db), CultRepository(db))
    return serializers.deity_to_schema(deity)

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
    return {"message": f"Entity {e.id}.{e.name} created."}

@app.get("/entity/{entity_id}", response_model=EntitySchema)
def get_entity(entity_id: int):
    entities_repo = EntityRepository(db)
    entity = entities_repo.get_without_cults(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    entities_repo.populate_entity_cults(entity, DeityRepository(db), CultRepository(db))
    return serializers.entity_to_schema(entity)

@app.post("/battle")
def initiate_battle(battle: Battle):
    entities_repo = EntityRepository(db)
    atk = entities_repo.get_without_cults(battle.attacker_id)
    defn = entities_repo.get_without_cults(battle.defender_id)
    if not atk or not defn:
        return {"error": "Invalid attacker or defender"}
    atk.attack(defn)
    entities_repo.save_without_cults(atk)
    entities_repo.save_without_cults(defn)
    db.commit()
    return {"message": f"Battle between {atk.name} and {defn.name} concluded."}

@app.post("/offering")
def make_offering(offering: Offering):
    entities_repo = EntityRepository(db)
    deities_repo = DeityRepository(db)
    cults_repo = CultRepository(db)
    entity = entities_repo.get_without_cults(offering.entity_id)
    entities_repo.populate_entity_cults(entity, deities_repo, cults_repo)
    deity = deities_repo.get_without_cults(offering.deity_id)
    if not entity or not deity:
        return {"error": "Invalid entity or deity"}
    entity.offer_to(deity, offering.amount)
    entities_repo.save_without_cults(entity)
    deities_repo.save_without_cults(deity)
    entities_repo.save_entity_cults(entity, cults_repo, deities_repo)
    db.commit()
    return {"message": f"{entity.name} offered {offering.amount} to {deity.name} (full offerings: {deity.melam()})."}

@app.get("/state")
def game_state():
    entities_repo = EntityRepository(db)
    deities_repo = DeityRepository(db)
    cults_repo = CultRepository(db)
    entities = entities_repo.list_all()
    deities = deities_repo.list_all()
    for entity in entities:
        entities_repo.populate_entity_cults(entity, deities_repo, cults_repo)
    for deity in deities:
        deities_repo.populate_deity_cults(deity, entities_repo, cults_repo)
    return {
        "entities": [serializers.entity_to_schema(e) for e in entities], # type: ignore
        "deities": [serializers.deity_to_schema(d) for d in deities]
    }