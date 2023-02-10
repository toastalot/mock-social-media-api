from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ...auth import AuthHandler

from ...database import getDB

from ...models import Posts
from .schemas import CreatePost, PostResponse, UpdatePost

router = APIRouter(tags=["Posts"])

authHandler = AuthHandler()

# todo - pagination
@router.get("/posts", response_model=List[PostResponse])
def getPosts(db: Session = Depends(getDB), authUser=Depends(authHandler.requireAuth)):
    posts = db.query(Posts).all()
    return posts


@router.post("/posts", status_code=201)
def createPosts(
    post: CreatePost,
    db: Session = Depends(getDB),
    authUser=Depends(authHandler.requireAuth),
):
    newPost = Posts(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


@router.get(
    "/posts/{id}",
    response_model=PostResponse,
)
def getPost(
    id: int, db: Session = Depends(getDB), authUser=Depends(authHandler.requireAuth)
):
    post = db.query(Posts).filter(Posts.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"post with id={id} was not found",
        )
    return post


@router.delete("/posts/{id}", status_code=204)
def deletePost(
    id: int, db: Session = Depends(getDB), authUser=Depends(authHandler.requireAuth)
):
    postQuery = db.query(Posts).filter(Posts.id == id)

    if not postQuery.first():
        raise HTTPException(
            status_code=404,
            detail=f"post with id={id} was not found",
        )
    else:
        postQuery.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204)


@router.put("/posts/{id}", response_model=PostResponse)
def updatePost(
    id: int,
    post: UpdatePost,
    db: Session = Depends(getDB),
    authUser=Depends(authHandler.requireAuth),
):
    postQuery = db.query(Posts).filter(Posts.id == id)
    oldPost = postQuery.first()
    if not oldPost:
        raise HTTPException(status_code=404, detail=f"post with id={id} does not exist")
    else:
        postQuery.update(post.dict(), synchronize_session=False)
        db.commit()
        return postQuery.first()
