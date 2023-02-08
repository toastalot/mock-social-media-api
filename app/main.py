import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from envVars import DB, DB_PASSWORD, DB_USER, HOST

from .database import Base, engine
from .routes.posts.router import router as postsRouter
from .routes.users.router import router as usersRouter
from .routes.login.router import router as loginRouter

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(postsRouter)
app.include_router(usersRouter)
app.include_router(loginRouter)
