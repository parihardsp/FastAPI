# --BOOK-5
"""
Assignment

Here is your opportunity to keep learning!

We are going to create a fake authentication model for our project 2  :)


    Modify our API book_login, so that it will consume an API header, that will have a username  attribute and a
    password attribute, and it will receive a query parameter of which book the user wants to read.

    The username submitted must be called FastAPIUser and the password submitted must be test1234!

    If both the username and password are valid, return the book located specified by the query parameter

    If either username or password is invalid, return Invalid User

    Call this new function after calling the  read_all_books just to make sure we have set up a fake inventory

"""
import uuid
from typing import Optional
# Pydantic is a Python library for data parsing and validation.
from uuid import UUID

from fastapi import FastAPI, Request, Header,Form
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description",
                                       min_length=1,
                                       max_length=100)
    rating: int = Field(gt=-1, le=100)

    class Config:
        json_schema_extra = {
            "example": dict(id="2bbadd1a-151c-43f4-876a-e1d7ad3667f1", title="Data Tech Fusion-ist", author="Author D",
                            description="Data with Tech", rating=90)
        }
    # Creates new example value under the request body.


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(title="Description",
                                       min_length=1,
                                       max_length=100)


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey,Why do you want {exception.books_to_return}"
                            f"books?, You need to read more!"}
    )


# optional not working , author=Optional[str]=None is working.
@app.get("/")
async def real_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        await create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:  # books_to_return can be optional
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    else:
        return {'detail': 'No UUID exist of such combination'}


async def create_books_no_api():
    # Book 1
    book_1 = Book(
        id="2bbadd1a-151c-43f4-876a-e1d7ad3667f1",
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=99
    )

    # Book 2
    book_2 = Book(
        id="3a8df590-762d-4c32-81d9-c7b248812345",
        title="Title 2",
        author="Author 2",
        description="Description 2",
        rating=85
    )

    # Book 3
    book_3 = Book(
        id="5d9361ca-8e87-4d58-90b7-2b24eb1abcde",
        title="Title 3",
        author="Author 3",
        description="Description 3",
        rating=95
    )

    # Book 4
    book_4 = Book(
        id="8e153d16-7e47-4a0c-9a9b-1427d7867890",
        title="Title 4",
        author="Author 4",
        description="Description 4",
        rating=88
    )

    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


#assignment.

@app.post("/books/login/")
async def book_login(book_id: UUID, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):  # Here book_id will be referencing the location of the book within the list of books, not uuid of book
    if username=='User' and password=='test123':
        counter=0
        for x in BOOKS:
            counter += 1
            if x.id == book_id:
                return BOOKS[counter-1] ,'Books is here'
            else:
                return ('UUID dosent Exist')

    return 'Invalid user'
