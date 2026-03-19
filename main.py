from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from db.engine import create_db_and_tables, SessionDep
from db.models import Post, PostCreate, PostPublic, PostUpdate
from sqlmodel import select

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/post", response_model=PostPublic)
def create_hero(post: PostCreate, session: SessionDep) -> Post:
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@app.get("/post", response_model=list[PostPublic])
def read_posts(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[Post]:
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts


@app.get("/post/{post_id}", response_model=PostPublic)
def read_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.patch("/post/{post_id}", response_model=PostPublic)
def update_post(post_id: int, post: PostUpdate, session: SessionDep):
    post_db = session.get(Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db


@app.delete("/post/{post_id}")
def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    raise HTTPException(status_code=204)
