from db.db import Base, engine
from db import models

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print("Done.")