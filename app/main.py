from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from envVars import DB, DB_PASSWORD, DB_USER, HOST

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# todo - deal with unstable connection
try:
    conn = psycopg2.connect(
        host=HOST,
        database=DB,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Connected to database")
except Exception as err:
    print(f"Could not connect to database: {err}")


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=201)
def createPosts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def getLatestPost():
    latest = myPosts[-1]
    return latest


@app.get("/posts/{id}")
def getPost(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"post with id={id} was not found",
        )
    return {"post": post}


@app.delete("/posts/{id}", status_code=204)
def deletePost(id: int):
    cursor.execute("""DELETE FROM posts WHERE id =  %s RETURNING *""", (id,))
    deletedPost = cursor.fetchone()
    conn.commit()
    if not deletedPost:
        raise HTTPException(
            status_code=404,
            detail=f"post with id={id} was not found",
        )
    return Response(status_code=204)


@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id),
    )
    updatedPost = cursor.fetchone()
    conn.commit()
    if not updatedPost:
        raise HTTPException(status_code=404, detail=f"post with id={id} does not exist")
    else:
        return {"data": updatedPost}
