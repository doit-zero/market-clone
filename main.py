from fastapi import FastAPI, UploadFile, Form, Response, Depends
from pydantic import BaseModel
from fastapi.staticfiles import (
    StaticFiles,
)  # astapi.staticfiles
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import sqlite3
import hashlib

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

SECRET = "super-coding"
manager = LoginManager(SECRET, "/login")


@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(
        f"""
                       SELECT * FROM user WHERE {WHERE_STATEMENTS}
                       """
    ).fetchone()
    return user


@app.post("/login")
def login(id: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = query_user(id)
    print(user)
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException

    # 액세스 토큰 만들기
    access_token = manager.create_access_token(
        data={"sub": {"name": user["name"], "email": user["email"], "id": user["id"]}}
    )
    # 프론트엔드에서 받을 수 있게 액세스토큰 리턴해주기
    return {"access_token": access_token}


@app.post("/signup")
def signup(
    id: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
):
    # 비밀번호 해쉬화
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute(
        f"""
                INSERT INTO user(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{hashed_password}')
                """
    )
    con.commit()
    print(hashed_password)
    return "200"


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
    user=Depends(manager),
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
async def get_items(user=Depends(manager)):
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


# 항상 app.mount 위에 작성해줘야함
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
