# import re

# def sanitize_barcode(data: str) -> str:
#     # Remove any non-alphanumeric characters to prevent injection
#     return re.sub(r'[^a-zA-Z0-9\-]', '', data)

# import bcrypt


# def hash_password(password: str) -> str:
#     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# def verify_password(password: str, hashed: str) -> bool:
#     return bcrypt.checkpw(password.encode(), hashed.encode())

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)