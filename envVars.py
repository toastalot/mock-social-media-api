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


HOST = getRequired("HOST")
DB = getRequired("DB")
DB_USER = getRequired("DB_USER")
DB_PASSWORD = getRequired("DB_PASSWORD")
