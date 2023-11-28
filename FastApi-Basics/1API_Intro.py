#--BOOK-1
#Basics of API, Get Method.

from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/")
async def real_all_books():
    return BOOKS


class DirectionName(Enum):
    north = "North"
    south = "South"
    east = 'East'
    west = 'West'


# , not req within the class.

@app.get('/direction/{dir_name}')
async def get_dir(dir_name: DirectionName):
    if dir_name == DirectionName.north:
        return {'Direction': dir_name, 'sub': 'up'}
    if dir_name == DirectionName.south:
        return {'Direction': dir_name, 'sub': 'down'}
    if dir_name == DirectionName.west:
        return {'Direction': dir_name, 'sub': 'left'}
    if dir_name == DirectionName.east:
        return {'Direction': dir_name, 'sub': 'right'}


@app.get("/books/mybook")
async def read_books():
    return {"Book-Title": 'My Fab Book'}


@app.get("/books/{book_id}")  #path parameter {book_id}
async def read_books(book_id: int):
    return {"Book-Title": BOOKS[book_id]}


# mybook  api should be before path parameters(which here is int)

@app.get('/{book_name}')
async def read_book(book_name: int):
    return BOOKS[book_name]


@app.get('/skip_book/}')
async def skip_book(id:int=3):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[id]
        return  new_books, {"Desc": f"We have Skipped {id} indexed data"}
    return BOOKS
# for now id is in the query parameter, you can access it as http://127.0.0.1:8000/skip_book/%7D?id=3


#Now if you put {id} in path parameter, then default value will not work.
# Eg. @app.get('/skip_book/{id}')
#async def skip_book(id: int =3): Defult int value.
#We can only keep str as Optional[str]=None, not int