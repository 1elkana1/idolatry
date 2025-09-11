from sqlalchemy.orm import Session
from app.db import models
from app.core.cults import Cult

class CultRepository:
    def __init__(self, db: Session):
        self.db = db
        self._cache = {}

    def get_by_id(self, cult_id, entities_repo, deities_repo) -> Cult | None:
        if cult_id in self._cache:
            return self._cache[cult_id]
        db_cult = self.db.get(models.CultDB, cult_id)
        if not db_cult:
            return None
        entity = entities_repo.get_without_cults(db_cult.entity_id)
        deity = deities_repo.get_without_cults(db_cult.deity_id)
        cult = Cult(entity, deity, db_cult.offerings, db_cult.id) # type: ignore
        self._cache[db_cult.id] = cult
        return cult

    def get_by_entity_and_deity(self, entity, deity) -> Cult | None:
        db_cult = self.db.query(models.CultDB).filter(
            models.CultDB.entity_id == entity.id,
            models.CultDB.deity_id == deity.id
        ).first()
        if not db_cult:
            return None
        if db_cult.id in self._cache:
            return self._cache[db_cult.id]
        cult = Cult(entity, deity, db_cult.offerings, db_cult.id) # type: ignore
        self._cache[db_cult.id] = cult
        return cult

    def save(self, cult: Cult):
        if not cult.entity.id or not cult.deity.id:
            raise ValueError("Both Entity and Deity must be saved before saving Cult")
        # item exists in DB:
        if cult.id:
            db_cult = self.db.get(models.CultDB, cult.id)
            if not db_cult:
                raise ValueError("Cult not found in DB")
            db_cult.offerings = cult.offerings # type: ignore
            self.db.flush()
            self._cache[cult.id] = cult
            return cult
        # new item:
        db_cult = models.CultDB(
            deity_id=cult.deity.id,
            entity_id=cult.entity.id,
            offerings=cult.offerings,
        )
        self.db.add(db_cult)
        self.db.flush()
        self.db.refresh(db_cult)
        cult.id = db_cult.id
        self._cache[cult.id] = cult
        return cult
        # no commit yet - dont forget to commit at the end of the batch