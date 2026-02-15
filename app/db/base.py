"""
Defines the base class for all SQLAlchemy ORM models.
All database models will inherit from this Base.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
