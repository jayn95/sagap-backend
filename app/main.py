from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api import agents, assets, assignments, reports  # import from api folder

app = FastAPI(title="SAGAP Inventory Backend")

@app.on_event("startup")
def on_startup():
    """Initialize DB tables"""
    Base.metadata.create_all(bind=engine)

# Include routers (prefix already in router files)
app.include_router(agents.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(reports.router)
