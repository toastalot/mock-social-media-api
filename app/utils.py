from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashSecret(secret: str):
    return pwdContext.hash(secret)


def verifySecret(secret, hashedSecret):
    return pwdContext.verify(secret, hashedSecret)
