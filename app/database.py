from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from envVars import DB, DB_PASSWORD, DB_USER, HOST

SQLALCHEMY_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}/{DB}"

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
