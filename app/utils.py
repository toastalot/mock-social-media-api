from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashSecret(secret: str):
    return pwdContext.hash(secret)
