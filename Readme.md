# Mock Social Media API

- built to practice using fastapi

 - currently uses psycopg2-binary which is a pre-compiled version of the C stuff, production builds should use psycopg which requires prerequisites listed at (https://www.psycopg.org/docs/install.html)

## Running App

# Dev
- If using new virtualenv then run `pip install wheel`
- install dependencies with `pip install -r requirements.txt`
- start postgres with `docker compose up postgres`
- start api with 


## Required Environment Variables

- `DB_HOST` - url for postgres instance
- `DB_NAME` - name of database
- `DB_USER` - database username
- `DB_PASSWORD` - database password
- `JWT_SECRET` - 256 bit secret creating JWT
- `ALLOWED_ORIGINS` - allowed origins for CORS policy, supply multiple in comma+space separated form a, b, c ...

- `POSTGRES_PASSWORD` - same as DB_PASSWORD, required to be present to make postgres container work, see https://hub.docker.com/_/postgres
- `POSTGRES_DB` - should be same as DB_USER, required to initialise a db

## Optional Environment Variables
- `DB_PORT` - port api and postgres container connect with when using docker-compose-dev.yml defaults to 5432
- `JWT_EXPIRY_MINUTES` - expiry for jwt, defaults to 30 if left unset
- `JWT_ALGORITHM` - hashing algorithm 