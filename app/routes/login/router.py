from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ...auth import AuthHandler
from ...models import Users
from .schemas import Credentials, Token
from ...database import getDB

router = APIRouter(tags=["Login"])

authHandler = AuthHandler()


@router.post("/login")
def login(credentials: Credentials, db: Session = Depends(getDB)):
    user = db.query(Users).filter(Users.email == credentials.email).first()

    if (not user) or (
        not authHandler.verifyPassword(credentials.password, user.password)
    ):
        raise HTTPException(status_code=403, detail="invalid login details")

    token = authHandler.encodeToken(user.id)
    return {"token": token}
