import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from envVars import DB, DB_PASSWORD, DB_USER, HOST

from .database import Base, engine
from .routes.posts.router import router as postsRouter
from .routes.users.router import router as usersRouter
from .routes.login.router import router as loginRouter
from .routes.like.router import router as likeRouter

app = FastAPI()

app.include_router(postsRouter)
app.include_router(usersRouter)
app.include_router(loginRouter)
app.include_router(likeRouter)
