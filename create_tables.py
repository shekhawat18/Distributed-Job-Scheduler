from app.db.database import Base, engine

# Import every model
from app.models import *

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")