# --BOOK-4

# Custom HTTP Exceptions

# Building Response Model, Using FastAPI to validate data and cahnges our data to specififc type decleration
'''
-making a silmiar book class, but remove the attribute which you dont want to include eg. here Rating
-make the get api with new path, in @app.get() decorator pass response_model= new Class
'''

# Creating custom Exception handler eg. NegativeNumberException for get method:
"""
Importing modules like from fastapi import HTTPException, Request, from starlette.responses import JSONResponse
Making Class of Negative Number Exception using Exception
Making function of Negative-no-handler using Request, JsonResponse
"""
# Adding own Stauts Code to response of an API
'''
-import status from fastapi
-Now add status_code in the requried api decorator, here @app.post("/",status_code=status.HTTP_201_CREATED"
'''

# Using Form Fields,passing Data (eg. Username-Password)
'''
-import form from fastapi
-creating post api @app.post("/books/login")
-now create the function passing un and pass using Form() field
'''

# Creating Headers
'''
-Header are a way that we can send additional info with each request
-As API recieves the headers, we can do wahtever we want the headers and do some kind of validation

In summary, the key difference between Form() and Header() is in how they handle data and where that data is expected to be in the request:

Form() is used for data in the request body, typically from form submissions.
Header() is used for data in the HTTP headers of the request, often for metadata or authentication information.
'''

from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
# Pydantic is a Python library for data parsing and validation.
from uuid import UUID
from typing import Optional
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


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(title="Description",
                                       min_length=1,
                                       max_length=100)


BOOKS = []


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
    # or raise raise_exception_error()


'''
Query parameter is by default unless and until it is not specified in the address
Now if path is query as @app.get("/book/"), then in address bar you have to navigate via:
http://127.0.0.1:8000/book?book_id=3a8df590-762d-4c32-81d9-c7b248812345

Else, if it has path parameter like:@app.get("/book/{book_id"), then nav via:
'http://127.0.0.1:8000/book/3a8df590-762d-4c32-81d9-c7b248812345'

'''


@app.get("/book/no-rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_exception_error()


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/update-book/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_exception_error()


@app.delete("/delete-book/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return {'detail': f'Book having id {book_id} deleted'}, BOOKS

    raise raise_exception_error()


# FormFields for username & password., using from fastapi import forms,headers
# When using form data, the data is typically encoded using the media type


@app.post("/books/login")
async def book_login(username: str = Form(), password: str = Form()):  # Can just write Form() in newer ver of FastAPI
    return {"USERNAME": username,
            "PASSWORD": password}


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None) ):
    return {'Random-Header': random_header}


async def create_books_no_api():
    # Book 1
    book_1 = Book(
        id="2bbadd1a-151c-43f4-876a-e1d7ad3667f1",
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=90
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


# Custom Exception

from fastapi import HTTPException, Request
from starlette.responses import JSONResponse


def raise_exception_error():
    return HTTPException(status_code=404,
                         detail='Book not found',
                         headers={'Header-Error': 'Nothing at this UUI'}
                         )


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


@app.exception_handler(NegativeNumberException)
async def negative_number_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey,Why do you want {exception.books_to_return} "
                            f"books?, You need to read more!"}
    )
