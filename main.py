from fastapi import FastAPI, UploadFile, Form, Response
from pydantic import BaseModel
from fastapi.staticfiles import (
    StaticFiles,
)  # astapi.staticfiles
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import sqlite3


con = sqlite3.connect("dbex.db", check_same_thread=False)
cur = con.cursor()

cur.execute(
    f"""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL
            );
            """
)


class Msg(BaseModel):
    id: str
    content: str


msgs = []

app = FastAPI()


@app.post("/msg")
def create_msg(msg: Msg):
    msgs.append(msg)


@app.get("/msg")
def read_msg():
    return msgs


@app.post("/items")
async def create_item(
    image: UploadFile,
    title: Annotated[str, Form()],
    price: Annotated[int, Form()],
    description: Annotated[str, Form()],
    place: Annotated[str, Form()],
    insertAt: Annotated[int, Form()],
):
    image_bytes = await image.read()
    cur.execute(
        f"""
                INSERT INTO items(title,image,price,description,place,insertAt)
                VALUES ('{title}','{image_bytes.hex()}','{price}','{description}','{place}','{insertAt}')
                """
    )
    con.commit()
    print("ehl?")
    return "200"


@app.get("/items")
async def get_items():
    # 컬럼명도 같이 가져오게 함
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(
        f"""
                       SELECT * from items;
                       """
    ).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))


@app.get("/images/{item_id}")
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(
        f"""
                              SELECT image from items WHERE id ={item_id}
                              """
    ).fetchone()[0]

    return Response(content=bytes.fromhex(image_bytes))


@app.post("/signup")
def signup(
    id: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
):
    cur.execute(
        f"""
                INSERT INTO user(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{password}')
                """
    )
    con.commit()
    return "200"


# 항상 app.mount 위에 작성해줘야함
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
