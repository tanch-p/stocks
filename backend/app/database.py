from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------
# 1. DATABASE URL
# --------------------------------------------------
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/mydb"

# --------------------------------------------------
# 2. CREATE DATABASE ENGINE
# --------------------------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,        # checks connection before using it
    pool_size=10,              # optional: control connection pool
    max_overflow=20
)

# --------------------------------------------------
# 3. CREATE SESSIONMAKER
# --------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --------------------------------------------------
# 4. BASE CLASS FOR MODELS
# --------------------------------------------------
Base = declarative_base()

# --------------------------------------------------
# 5. DEPENDENCY: get_db()
# --------------------------------------------------
def get_db():
    """
    Dependency that provides a database session to FastAPI routes.
    Yields a SQLAlchemy session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
