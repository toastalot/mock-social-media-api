from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...database import getDB
from ...models import Users
from ...utils import hashSecret

from .schemas import CreateUser, UserResponse

router = APIRouter(tags=["Users"])


@router.post("/users", status_code=201, response_model=UserResponse)
def createUser(user: CreateUser, db: Session = Depends(getDB)):
    hashedPwd = hashSecret(user.password)
    user.password = hashedPwd

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


@router.get("/users/{id}", response_model=UserResponse)
def getUser(id: int, db: Session = Depends(getDB)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"user with id={id} does not exist",
        )
    else:
        return user
