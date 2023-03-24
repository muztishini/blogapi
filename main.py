from typing import List
from fastapi import FastAPI
from bd import database, posts
from schemas import Post, PostIn

app = FastAPI(title="BlogApi")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/posts/', response_model=List[Post])
async def read_posts():
    query = posts.select()
    return await database.fetch_all(query)


@app.post("/posts/", response_model=Post)
async def create_post(post: PostIn):
    query = posts.insert().values(title=post.title, text=post.text, is_published=post.is_published)
    last_record_id = await database.execute(query)
    return {**post.dict(), "id": last_record_id}


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: PostIn):
    query = posts.update().where(posts.c.id == post_id).values(title=post.title,
                                                               text=post.text,
                                                               is_published=post.is_published)
    await database.execute(query)
    return {"detail": "Post update", "status_code": 204}


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    query = posts.delete().where(posts.c.id == post_id)
    await database.execute(query)
    return {"detail": "Post deleted", "status_code": 204}
