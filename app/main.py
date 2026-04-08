from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api import agents, assets, assignments, generated_document, audit, user  # import from api folder
from fastapi.middleware.cors import CORSMiddleware # For Electron CORS issues

app = FastAPI(title="SAGAP Inventory Backend")

@app.on_event("startup")
def on_startup():
    """Initialize DB tables"""
    Base.metadata.create_all(bind=engine)

# 3. Security: CORS Middleware (Allow Electron)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (prefix already in router files)
app.include_router(agents.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(generated_document.router)
app.include_router(audit.router)
app.include_router(user.router)