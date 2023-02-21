from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...models import Likes, Posts

from ...AuthHandler import AuthHandler
from ...database import getDB

from .schemas import Like

authHandler = AuthHandler()

router = APIRouter(tags=["like"])


@router.post("/like", status_code=201)
def like(
    like: Like,
    db: Session = Depends(getDB),
    currentUser=Depends(authHandler.getCurrentUser),
):
    post = db.query(Posts).filter(Posts.id == like.post_id).first()
    if post:
        likeQuery = db.query(Likes).filter(
            Likes.post_id == like.post_id, Likes.user_id == currentUser["id"]
        )
        foundLike = likeQuery.first()
        if like.action:
            if foundLike:
                raise HTTPException(
                    status_code=409,
                    detail=f'user {currentUser["id"]} has already liked post {like.post_id}',
                )
            newLike = Likes(post_id=like.post_id, user_id=currentUser["id"])
            db.add(newLike)
            db.commit()
            return {"message": "successfully liked post"}
        else:
            if not foundLike:
                raise HTTPException(status_code=404, detail=f"like does not exist")
            likeQuery.delete(synchronize_session=False)
            db.commit()
            return {"message": "successfully deleted like"}
    else:
        raise HTTPException(
            status_code=404, detail=f"post with id={like.post_id} does not exist"
        )
