import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text
from app.core.config import settings

def test_migrations_upgrade():
    # Create a test database URL
    test_db_url = settings.SQLALCHEMY_DATABASE_URI + "_test"
    
    # Create test database
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS pledge_test"))
        conn.execute(text("CREATE DATABASE pledge_test"))
    
    # Configure Alembic
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    
    # Run migrations
    command.upgrade(alembic_cfg, "head")
    
    # Verify tables exist
    engine = create_engine(test_db_url)
    with engine.connect() as conn:
        # Check users table
        result = conn.execute(text("SHOW TABLES LIKE 'users'"))
        assert result.fetchone() is not None
        
        # Check members table
        result = conn.execute(text("SHOW TABLES LIKE 'members'"))
        assert result.fetchone() is not None
        
        # Check groups table
        result = conn.execute(text("SHOW TABLES LIKE 'groups'"))
        assert result.fetchone() is not None
        
        # Check projects table
        result = conn.execute(text("SHOW TABLES LIKE 'projects'"))
        assert result.fetchone() is not None
        
        # Check contributions table
        result = conn.execute(text("SHOW TABLES LIKE 'contributions'"))
        assert result.fetchone() is not None
        
        # Check sms table
        result = conn.execute(text("SHOW TABLES LIKE 'sms'"))
        assert result.fetchone() is not None

def test_migrations_downgrade():
    # Create a test database URL
    test_db_url = settings.SQLALCHEMY_DATABASE_URI + "_test"
    
    # Create test database
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS pledge_test"))
        conn.execute(text("CREATE DATABASE pledge_test"))
    
    # Configure Alembic
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    
    # Run migrations up
    command.upgrade(alembic_cfg, "head")
    
    # Run migrations down
    command.downgrade(alembic_cfg, "base")
    
    # Verify tables don't exist
    engine = create_engine(test_db_url)
    with engine.connect() as conn:
        # Check users table
        result = conn.execute(text("SHOW TABLES LIKE 'users'"))
        assert result.fetchone() is None
        
        # Check members table
        result = conn.execute(text("SHOW TABLES LIKE 'members'"))
        assert result.fetchone() is None
        
        # Check groups table
        result = conn.execute(text("SHOW TABLES LIKE 'groups'"))
        assert result.fetchone() is None
        
        # Check projects table
        result = conn.execute(text("SHOW TABLES LIKE 'projects'"))
        assert result.fetchone() is None
        
        # Check contributions table
        result = conn.execute(text("SHOW TABLES LIKE 'contributions'"))
        assert result.fetchone() is None
        
        # Check sms table
        result = conn.execute(text("SHOW TABLES LIKE 'sms'"))
        assert result.fetchone() is None

def test_migrations_revision():
    # Configure Alembic
    alembic_cfg = Config("alembic.ini")
    
    # Get current revision
    current_rev = command.current(alembic_cfg)
    assert current_rev is not None
    
    # Get revision history
    history = command.history(alembic_cfg)
    assert len(history) > 0
    
    # Get head revision
    head_rev = command.heads(alembic_cfg)
    assert len(head_rev) == 1
    assert head_rev[0] == current_rev

def test_migrations_autogenerate():
    # Create a test database URL
    test_db_url = settings.SQLALCHEMY_DATABASE_URI + "_test"
    
    # Create test database
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS pledge_test"))
        conn.execute(text("CREATE DATABASE pledge_test"))
    
    # Configure Alembic
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    
    # Run migrations up
    command.upgrade(alembic_cfg, "head")
    
    # Make some changes to the database schema
    engine = create_engine(test_db_url)
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE users ADD COLUMN test_column VARCHAR(255)"))
    
    # Generate a new migration
    command.revision(alembic_cfg, autogenerate=True, message="Add test column")
    
    # Verify the new migration file was created
    import os
    migrations_dir = "alembic/versions"
    migration_files = [f for f in os.listdir(migrations_dir) if f.endswith("_add_test_column.py")]
    assert len(migration_files) == 1
    
    # Clean up
    os.remove(os.path.join(migrations_dir, migration_files[0]))

def test_migrations_data_preservation():
    # Create a test database URL
    test_db_url = settings.SQLALCHEMY_DATABASE_URI + "_test"
    
    # Create test database
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS pledge_test"))
        conn.execute(text("CREATE DATABASE pledge_test"))
    
    # Configure Alembic
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    
    # Run migrations up
    command.upgrade(alembic_cfg, "head")
    
    # Insert test data
    engine = create_engine(test_db_url)
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO users (email, hashed_password, full_name, role) VALUES ('test@example.com', 'test_hash', 'Test User', 'STAFF')"))
    
    # Run migrations down and up again
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
    
    # Verify data is preserved
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = 'test@example.com'"))
        user = result.fetchone()
        assert user is not None
        assert user.full_name == "Test User"
        assert user.role == "STAFF" 