from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from databases import Database

DATABASE_URL = "postgresql://username:password@localhost/dbname"

app = FastAPI()
database = Database(DATABASE_URL)
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.post("/tickets")
async def create_ticket(ticket: Ticket, db: Session = Depends(get_db)):
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
