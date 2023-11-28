#--BOOK-3

#Using Pydantic Lib for data parsing and validation.
'''
-Making class from BaseModel (Structure of a Book)
-Appending Books Dict in BOOKS list
-
'''


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
# Pydantic is a Python library for data parsing and validation.
from uuid import UUID, uuid4
from typing import Optional

app = FastAPI()


class Book(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Use default_factory to generate a unique UUID
    title: str = Field(min_length=1)
    author: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description",
                                       min_length=1,
                                       max_length=100)
    rating: int = Field(gt=-1, le=100)

    class Config:
        json_schema_extra = {
            "example": dict(id="2bbadd1a-151c-43f4-876a-e1d7ad3667f1",
                            title="Data Tech Fusion-ist",
                            author="Author D",
                            description="Data with Tech",
                            rating=90)
        }
    # Creates new example value under the request body.



BOOKS = []


# optional not working , author=Optional[str]=None is working.
@app.get("/")
async def real_all_books(books_to_return: Optional[int] = None):
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
    # raise HTTPException(status_code=404,detail='Book not found',
    #                            headers={'Header-Error':'Nothing at this UUID'})


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


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


def raise_exception_error() -> object:
    return HTTPException(status_code=404,
                         detail='Book not found',
                         headers={'Header-Error': 'Nothing at this UUI'}
                         )
