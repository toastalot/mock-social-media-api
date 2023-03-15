from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from envVars import DB_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER

SQLALCHEMY_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
