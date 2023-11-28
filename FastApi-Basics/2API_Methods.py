#--BOOK-2

#Post / Put / Delete

from fastapi import FastAPI
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


# @app.get("/books/mybook")
# async def read_books():
#     return {"Book-Title": 'My Fab Book'}


@app.get("/books/{book_id}")
async def read_books(book_id: int):
    return {"Book-Title": BOOKS[book_id]['title']}

@app.post("/add-book/{book_id}")
async def create_book(book_title,book_author,category):
    content={'title': book_title, 'author': book_author, 'category': category}
    BOOKS.append(content)
    return 'Book is entered successfully', content

@app.put('/update-book/{book_id}')
async def update_book(book_id:int,book_title: str,book_author:str,category:str):
    book_info={'title': book_title, 'author': book_author, 'category': category}
    BOOKS[book_id]=book_info
    return BOOKS

@app.delete('/delete-book/{book_id}')
async def delete_book(book_id:int):
    title = BOOKS[book_id]['title']
    del BOOKS[book_id]
    return f'Book with title {title} is successfully delated'

#----------------------------------------------------------#
'''
Path Parameters:They are in the url itself
Query Parametrs: They are added at the end of the url with a ? , then it will have variable and a value
'''

#making get and delete method using Query parameters.
@app.get("/assignment/") #/ at end suggest its a query parameter.
async def read_book_assign(book_id:int):
    return {"Book-Title": BOOKS[book_id]['title']}


@app.delete('/assignment/')
async def delete_book(book_id:int):
    title = BOOKS[book_id]['title']
    del BOOKS[book_id]
    return f'Book with title {title} is successfully delated'

#okok


