from sqlalchemy.orm import Session
from db import models
from core.entities import Entity

class EntityRepository:
    def __init__(self, db: Session):
        self.db = db
        self._cache = {}

    def get_without_cults(self, entity_id) -> Entity | None:
        if entity_id in self._cache:
            return self._cache[entity_id]
        db_entity = self.db.get(models.EntityDB, entity_id)
        if not db_entity:
            return None
        entity = Entity(
            name=db_entity.name,
            army=db_entity.army, # type: ignore
            wealth=db_entity.wealth, # type: ignore
            id=db_entity.id,
        )
        self._cache[entity_id] = entity
        return entity
    
    def populate_entity_cults(self, entity, deities_repo, cults_repo):
        db_entity = self.db.get(models.EntityDB, entity.id)
        db_cults = db_entity.cults if db_entity else []
        for db_cult in db_cults:
            cult = cults_repo.get_by_id(db_cult.id, self, deities_repo)
            cult.offerings = db_cult.offerings
            entity.add_cult(cult)

    def list_all(self):
        db_entities = self.db.query(models.EntityDB).all()
        return [self.get_without_cults(e.id) for e in db_entities]

    def save_without_cults(self, entity: Entity):
        # item exists in DB:
        if entity.id:
            db_entity = self.db.get(models.EntityDB, entity.id)
            if not db_entity:
                raise ValueError("Entity not found in DB")
            db_entity.army = entity.army # type: ignore
            db_entity.wealth = entity.wealth # type: ignore
            self.db.flush()
            self._cache[entity.id] = entity
            return entity
        # new item:
        db_entity = models.EntityDB(
            name=entity.name,
            army=entity.army,
            wealth=entity.wealth,
        )
        self.db.add(db_entity)
        self.db.flush()
        self.db.refresh(db_entity)
        entity.id = db_entity.id
        self._cache[entity.id] = entity
        return entity
        # no commit yet - dont forget to commit at the end of the batch
    
    def save_entity_cults(self, entity, cults_repo, deities_repo):
        for cult in entity.cults:
            deities_repo.save_without_cults(cult.deity)
            cults_repo.save(cult)
        return entity
