from app.db.base import Base
from app.db.database import engine
from app.db.models import User


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")