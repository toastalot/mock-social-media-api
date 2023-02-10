import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from envVars import JWT_ALGORITHM, JWT_EXPIRY_MINUTES, JWT_SECRET

from datetime import datetime, timedelta


class AuthHandler:
    security = HTTPBearer()
    pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = JWT_SECRET

    def getPasswordHash(self, password):
        return self.pwdContext.hash(password)

    def verifyPassword(self, plainPassword, hashedPassword):
        return self.pwdContext.verify(plainPassword, hashedPassword)

    def encodeToken(self, userId):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRY_MINUTES),
            "iat": datetime.utcnow(),
            "user": userId,
        }
        return jwt.encode(payload, self.secret, algorithm=JWT_ALGORITHM)

    def decodeToken(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[JWT_ALGORITHM])
            return payload["user"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def requireAuth(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decodeToken(auth.credentials)
