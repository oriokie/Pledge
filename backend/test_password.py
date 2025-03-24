from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User
from app.core.security import verify_password

# Create database connection
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Get the admin user
user = db.query(User).filter(User.phone_number == "+254700000000").first()
if user:
    print(f"Found user: {user.phone_number}")
    print(f"Password verification result: {verify_password('admin123', user.hashed_password)}")
else:
    print("User not found")

db.close() 