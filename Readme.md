# Mock Social Media API

- built to practice using fastapi

 - currently uses psycopg2-binary which is a pre-compiled version of the C stuff, production builds should use psycopg which requires prerequisites listed at (https://www.psycopg.org/docs/install.html)

## Required Environment Variables
- HOST - database url
- DB - name of database
- DB_USER - databse username
- DB_PASSWORD - database password
- JWT_SECRET - 256 bit secret creating JWT
- ALLOWED_ORIGINS - allowed origins for CORS policy, supply multiple in form a, b, c ...

## Other Environment Variables
- JWT_EXPIRY_MINUTES - expiry for jwt, defaults to 30 if left unset
- JWT_ALGORITHM - hashing algorithm 