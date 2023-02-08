# Mock Social Media API

- built to practice using fastapi

 - currently uses psycopg2-binary which is a pre-compiled version of the C stuff, production builds should use psycopg which requires prerequisites listed at (https://www.psycopg.org/docs/install.html)

## Required Environment Variables
- HOST - database url
- DB - name of database
- DB_USER
- DB_PASSWORD 
- JWT_SECRET - 256 bit secret creating JWT