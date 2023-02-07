from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import getDB
from .models import Users
from app.utils import hashSecret

from .schemas import CreateUser, UserResponse

router = APIRouter()


@router.post("/users", status_code=201, response_model=UserResponse)
def createUser(user: CreateUser, db: Session = Depends(getDB)):
    hashedPwd = hashSecret(user.password)
    user.password = hashedPwd

    newUser = Users(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
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
