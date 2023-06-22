from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, index=True)
    created_by = Column(String)

Base.metadata.create_all(bind=engine)
