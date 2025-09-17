from pydantic import BaseModel

class CultSchema(BaseModel):
    deity_id: int
    deity_name: str
    entity_id: int
    entity_name: str
    offerings: int

class DeitySchema(BaseModel):
    id: int
    name: str
    domain: str
    cults: list[CultSchema]

class EntitySchema(BaseModel):
    id: int
    name: str
    army: int
    wealth: int
    patron_id: int | None
    patron_name: str | None
    cults: list[CultSchema]