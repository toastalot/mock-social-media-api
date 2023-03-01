import os
from dotenv import load_dotenv

load_dotenv()


class MissingEnvironmentVariable(Exception):
    pass


def getRequired(name: str):
    envVar = os.environ.get(name)
    if envVar != 0 and not envVar:
        raise MissingEnvironmentVariable(f"Could not find required variable: {name}")
    else:
        return envVar


# DB
HOST = getRequired("HOST")
DB = getRequired("DB")
DB_USER = getRequired("DB_USER")
DB_PASSWORD = getRequired("DB_PASSWORD")

# OAUTH2
JWT_SECRET = getRequired("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM") or "HS256"
JWT_EXPIRY_MINUTES = float(os.environ.get("TOKEN_EXPIRY") or 30)

# CORS
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS").split(",")
