from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# API Endpoints
# -----------------------------

# ---------- CREATE ----------
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user.
    """
    return user_service.create_user(
        db,
        user,
        performed_by=1  # TEMPORARY USER ID
    )


# ---------- READ ALL ----------
@router.get("/", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    """
    Retrieves all users.
    """
    return user_service.get_all_users(db)


# ---------- READ ONE ----------
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single user by ID.
    """
    return user_service.get_user_by_id(db, user_id)

# ---------- LOGIN ----------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = user_service.login_user(db, user.username, user.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return result