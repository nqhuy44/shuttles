import os
from sqlalchemy import create_engine

def get_engine():
    """
    Creates and returns a SQLAlchemy engine based on the DATABASE_URL environment variable.
    Ensures that no hardcoded credentials are used.
    """
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set. Please set it to connect to the database.")
    return create_engine(db_url)
