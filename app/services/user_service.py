from sqlalchemy.orm import Session
from app.db import models
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from app.services.audit_service import log_action
from app.utils.security import verify_password
from app.utils.token import create_access_token

def create_user(db: Session, user: UserCreate, performed_by: int | None = None):
    hashed_pw = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        password_hash=hashed_pw,
        full_name=user.full_name,
        role=user.role,
        eid=user.eid
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # AUDIT LOG
    log_action(
        db=db,
        action="CREATE_USER",
        entity="USER",
        entity_id=new_user.id,
        performed_by=None,  # system for now
        details=f"Created user {new_user.username}"
    )

    return new_user


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# AUTTHENTICATION & LOGIN
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def login_user(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)

    if not user:
        return None

    token = create_access_token({
        "sub": str(user.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }