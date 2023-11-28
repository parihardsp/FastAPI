
from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, todos, users, address
from company import company_apis,dependencies

from starlette.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(company_apis.router,
                   prefix="/company_apis",
                   tags=["company_apis"],
                   dependencies=[Depends(dependencies.get_header_token)],
                   responses={418: {"description":"Internal Use Only"}})

app.include_router(users.router)
app.include_router(address.router)