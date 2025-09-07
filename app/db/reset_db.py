from app.db.db import Base, engine
from app.db import models  # make sure all models are imported

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print("Done.")