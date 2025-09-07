from app.core.entities import Entity
from app.core.deities import Deity
from app.db.db import SessionLocal
from app.db import mappers

db = SessionLocal()

# create core objects
enlil = Deity("Enlil", "War")
nippur = Entity("Nippur", enlil)

# do some game logic
nippur.recruit_army(20)
nippur.offer_to(enlil, 30)

# save to DB
mappers.save_entity(db, nippur)
mappers.save_deity(db, enlil)

# load back
loaded_nippur = mappers.load_entity(db, 1)
if loaded_nippur:
    print("Loaded from DB:", loaded_nippur.name, loaded_nippur.wealth, loaded_nippur.army)

db.close()
