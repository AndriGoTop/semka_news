from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

db_url = f"postgresql://postgres:Herfdbwf2006@127.0.0.1:5432/posts"

engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
