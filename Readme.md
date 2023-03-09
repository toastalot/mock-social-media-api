# Mock Social Media API

- built to practice using fastapi

 - currently uses psycopg2-binary which is a pre-compiled version of the C stuff, production builds should use psycopg which requires prerequisites listed at (https://www.psycopg.org/docs/install.html)

## Required Environment Variables
- HOST - database url
- DB - name of database
- DB_USER - database username
- DB_PASSWORD - database password
- JWT_SECRET - 256 bit secret creating JWT
- ALLOWED_ORIGINS - allowed origins for CORS policy, supply multiple in form a, b, c ...

## Required if running with docker compose
- POSTGRES_PASSWORD - same as DB_PASSWORD, required to be present to make postgres container work, see https://hub.docker.com/_/postgres
- POSTGRES_DB - same as DB_USER, required to initialise a db for api

## Other Environment Variables
- JWT_EXPIRY_MINUTES - expiry for jwt, defaults to 30 if left unset
- JWT_ALGORITHM - hashing algorithm 