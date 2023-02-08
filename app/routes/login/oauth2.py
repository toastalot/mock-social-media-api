from datetime import datetime, timedelta
from jose import jwt

from envVars import JWT_ALGORITHM, JWT_EXPIRY_MINUTES, JWT_SECRET


def createJWT(data: dict):
    toEncode = data.copy()
    expireyTime = datetime.now() + timedelta(minutes=JWT_EXPIRY_MINUTES)
    toEncode.update({"exp": expireyTime})
    return jwt.encode(toEncode, JWT_SECRET, algorithm=JWT_ALGORITHM)
