from app.db.session import engine
from app.db.base import Base

# ⚠ WARNING: This will DELETE ALL DATA in your tables
print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Recreating all tables...")
Base.metadata.create_all(bind=engine)

print("✅ Database reset complete!")
