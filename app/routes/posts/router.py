from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ...AuthHandler import AuthHandler

from ...database import getDB

from ...models import Posts
from .schemas import CreatePost, PostResponse, UpdatePost

router = APIRouter(tags=["Posts"])

authHandler = AuthHandler()

# todo - pagination
@router.get("/posts", response_model=List[PostResponse])
def getPosts(
    db: Session = Depends(getDB), currentUser=Depends(authHandler.getCurrentUser)
):
    posts = db.query(Posts).all()
    return posts


@router.post("/posts", status_code=201)
def createPosts(
    post: CreatePost,
    db: Session = Depends(getDB),
    currentUser=Depends(authHandler.getCurrentUser),
):
    newPost = Posts(**post.dict(), owner_id=currentUser["id"])
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


@router.get(
    "/posts/{id}",
    response_model=PostResponse,
)
def getPost(
    id: int,
    db: Session = Depends(getDB),
    currentUser=Depends(authHandler.getCurrentUser),
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
    id: int,
    db: Session = Depends(getDB),
    currentUser=Depends(authHandler.getCurrentUser),
):
    postQuery = db.query(Posts).filter(Posts.id == id)
    post = postQuery.first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"post with id={id} was not found",
        )
    if currentUser["id"] != post.owner_id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    else:
        postQuery.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204)


@router.put("/posts/{id}", response_model=PostResponse)
def updatePost(
    id: int,
    post: UpdatePost,
    db: Session = Depends(getDB),
    currentUser=Depends(authHandler.getCurrentUser),
):
    postQuery = db.query(Posts).filter(Posts.id == id)
    oldPost = postQuery.first()
    if not oldPost:
        raise HTTPException(status_code=404, detail=f"post with id={id} does not exist")
    print(currentUser["id"])
    print(oldPost.id)
    if currentUser["id"] != oldPost.owner_id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    postQuery.update(post.dict(), synchronize_session=False)
    db.commit()
    return postQuery.first()
