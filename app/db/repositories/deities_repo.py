from sqlalchemy.orm import Session
from db import models
from core.deities import Deity

class DeityRepository:
    def __init__(self, db: Session):
        self.db = db
        self._cache = {}

    def get_without_cults(self, deity_id) -> Deity | None:
        if deity_id in self._cache:
            return self._cache[deity_id]
        db_deity = self.db.get(models.DeityDB, deity_id)
        if not db_deity:
            return None
        deity = Deity(
            name=db_deity.name,
            domain=db_deity.domain,
            id=db_deity.id,
        )
        self._cache[deity_id] = deity
        return deity
    
    def populate_deity_cults(self, deity, entities_repo, cults_repo):
        db_deity = self.db.get(models.DeityDB, deity.id)
        db_cults = db_deity.cults if db_deity else []
        for db_cult in db_cults:
            cult = cults_repo.get_by_id(db_cult.id, entities_repo, self)
            cult.offerings = db_cult.offerings
            deity.add_cult(cult)
    
    def list_all(self):
        db_deities = self.db.query(models.DeityDB).all()
        return [self.get_without_cults(d.id) for d in db_deities]

    def save_without_cults(self, deity: Deity):
        # item exists in DB:
        if deity.id:
            db_deity = self.db.get(models.DeityDB, deity.id)
            if not db_deity:
                raise ValueError("Deity not found in DB")
            self.db.flush()
            self._cache[deity.id] = deity
            return deity
        # new item:
        db_deity = models.DeityDB(
            name=deity.name,
            domain=deity.domain,
        )
        self.db.add(db_deity)
        self.db.flush()
        self.db.refresh(db_deity)
        deity.id = db_deity.id
        self._cache[deity.id] = deity
        return deity
        # no commit yet - dont forget to commit at the end of the batch

    def save_deity_cults(self, deity, cults_repo, entities_repo):
        for cult in deity.cults:
            entities_repo.save(cult.entity)
            cults_repo.save(cult)
        return deity
