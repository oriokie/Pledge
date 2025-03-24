import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from app.core.security import get_password_hash
from datetime import datetime, UTC

def create_admin_user(session) -> None:
    """
    Create the first admin user if it doesn't exist.
    
    Args:
        session: SQLAlchemy database session
    """
    # Check if admin user exists
    admin = session.query(User).filter(User.phone_number == "+254700000000").first()
    
    if not admin:
        admin = User(
            phone_number="0700000000",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),  # Change this in production!
            role="ADMIN",
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        session.add(admin)
        session.commit()
        print("Created admin user")
    else:
        print("Admin user already exists")

def init_db(database_url: str, database_name: str) -> None:
    """
    Initialize a database by creating it if it doesn't exist and creating all tables.
    
    Args:
        database_url: The base database URL (without database name)
        database_name: The name of the database to create/initialize
    """
    # Create database URL with the specific database name
    db_url = f"{database_url}/{database_name}"
    
    # Create engine without database name to connect to postgres
    engine = create_engine(database_url)
    
    try:
        # Create database if it doesn't exist
        with engine.connect() as conn:
            conn.execute(text("COMMIT"))  # Close any open transactions
            conn.execute(text(f"CREATE DATABASE {database_name}"))
            print(f"Created database: {database_name}")
    except Exception as e:
        print(f"Database {database_name} might already exist: {str(e)}")
    
    # Create engine with database name to create tables
    engine = create_engine(db_url)
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print(f"Created all tables in database: {database_name}")
        
        # Create session and admin user
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        create_admin_user(session)
        session.close()
        
    except Exception as e:
        print(f"Error initializing database {database_name}: {str(e)}")
        sys.exit(1)

def main():
    """Initialize both test and production databases."""
    # Get the base database URL (without database name)
    base_db_url = str(settings.SQLALCHEMY_DATABASE_URI).rsplit("/", 1)[0]
    
    # Initialize production database
    print("\nInitializing production database...")
    init_db(base_db_url, "pledge")
    
    # Initialize test database
    print("\nInitializing test database...")
    init_db(base_db_url, "test_pledge")

if __name__ == "__main__":
    main() 