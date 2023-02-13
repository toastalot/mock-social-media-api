from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...database import getDB
from ...models import Users

from .schemas import CreateUser, User
from ...AuthHandler import AuthHandler

router = APIRouter(tags=["Users"])

authHandler = AuthHandler()


@router.post("/users", status_code=201, response_model=User)
def createUser(
    user: CreateUser,
    db: Session = Depends(getDB),
):

    user.password = authHandler.getPasswordHash(user.password)

    newUser = Users(**user.dict())
    db.add(newUser)
    try:
        db.commit()
        db.refresh(newUser)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail=f"email {newUser.email} is already in use"
        )
    else:
        return newUser


@router.get("/users/{id}", response_model=User)
def getUser(
    id: int,
    db: Session = Depends(getDB),
    currentUser=Depends(authHandler.getCurrentUser),
):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"user with id={id} does not exist",
        )
    else:
        return user
