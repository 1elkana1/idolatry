from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class EntityDB(Base):
    __tablename__ = "entities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    wealth = Column(Integer)
    army = Column(Integer)
    cults = relationship("CultDB", back_populates="entity")

class DeityDB(Base):
    __tablename__ = "deities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    domain = Column(String)
    cults = relationship("CultDB", back_populates="deity")

class CultDB(Base):
    __tablename__ = "cults"
    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"))
    deity_id = Column(Integer, ForeignKey("deities.id"))
    offerings = Column(Integer, default=0)
    entity = relationship("EntityDB", back_populates="cults")
    deity = relationship("DeityDB", back_populates="cults")