from random import randrange
from typing import List, Optional
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, getDB

from envVars import DB, DB_PASSWORD, DB_USER, HOST

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


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


# todo - pagination
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(getDB)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=201)
def createPosts(post: schemas.PostCreate, db: Session = Depends(getDB)):
    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def getPost(id: int, db: Session = Depends(getDB)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"post with id={id} was not found",
        )
    return post


@app.delete("/posts/{id}", status_code=204)
def deletePost(id: int, db: Session = Depends(getDB)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)

    if not postQuery.first():
        raise HTTPException(
            status_code=404,
            detail=f"post with id={id} was not found",
        )
    else:
        postQuery.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def updatePost(id: int, post: schemas.PostUpdate, db: Session = Depends(getDB)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    oldPost = postQuery.first()
    if not oldPost:
        raise HTTPException(status_code=404, detail=f"post with id={id} does not exist")
    else:
        postQuery.update(post.dict(), synchronize_session=False)
        db.commit()
        return postQuery.first()
