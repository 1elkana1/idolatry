from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# using sqlite for prototype (file-based dp stored locally in: game.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./game.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()