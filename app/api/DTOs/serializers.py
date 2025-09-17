from api.DTOs.schemas import EntitySchema, DeitySchema, CultSchema
from core.entities import Entity

def entity_to_schema(entity: Entity) -> EntitySchema:
    if not entity.id:
        raise ValueError("Entity have no ID - not persisted?")
    patron = entity.patron()
    return EntitySchema(
        id=entity.id,
        name=entity.name,
        army=entity.army,
        wealth=entity.wealth,
        patron_id=patron.id if patron else None,
        patron_name=patron.name if patron else None,
        cults=[cult_to_schema(cult) for cult in entity.cults]
    )

def deity_to_schema(deity) -> DeitySchema:
    if not deity.id:
        raise ValueError("Deity have no ID - not persisted?")
    return DeitySchema(
        id=deity.id,
        name=deity.name,
        domain=deity.domain,
        cults=[cult_to_schema(cult) for cult in deity.cults]
    )

def cult_to_schema(cult) -> CultSchema:
    if not cult.id:
        raise ValueError("Cult have no ID - not persisted?")
    return CultSchema(
        deity_id=cult.deity.id,
        deity_name=cult.deity.name,
        entity_id=cult.entity.id,
        entity_name=cult.entity.name,
        offerings=cult.offerings,
    )
