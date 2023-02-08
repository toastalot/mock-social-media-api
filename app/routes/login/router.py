from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .schemas import Login
from ...database import getDB
from ...models import Users
from ...utils import verifySecret
from .oauth2 import createJWT

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(userCredentials: Login, db: Session = Depends(getDB)):
    user = db.query(Users).filter(Users.email == userCredentials.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    if not verifySecret(userCredentials.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")

    jwt = createJWT(data={"userId": user.id})
    return {"access_token": jwt, "token_type": "bearer"}
