import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from envVars import DB, DB_PASSWORD, DB_USER, HOST

from .database import Base, engine
from .posts.router import router as postsRouter
from .users.router import router as usersRouter

app = FastAPI()

Base.metadata.create_all(bind=engine)


# todo - deal with unstable connection
try:
    conn = psycopg2.connect(
        host=HOST,
        database=DB,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Connected to database")
except Exception as err:
    print(f"Could not connect to database: {err}")

app.include_router(postsRouter)
app.include_router(usersRouter)
