import sys
sys.path.append("...")

from typing import Optional
from fastapi import Depends, APIRouter
import models
from TodoApp.database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={404: {"Address": "Not Found"}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    postalcode: str
    country: str
    apt_number:str

@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Address).all()

@router.post("/create")
async def read_all(address: Address,
                   user: dict = Depends(get_current_user),
                   db: Session = Depends(get_db),
                   ):
    if user is None:
        raise get_user_exception()

    address_model= models.Address()

    if address_model is None:

        address_model.address1= address.address1
        address_model.address2 = address.address2
        address_model.city = address.city
        address_model.state = address.state
        address_model.postalcode = address.postalcode
        address_model.country = address.country
        address_model.apt_number=address.apt_number

        db.add(address_model)
        db.flush()   #instead of commit, it will attach an id to it

        user_model= db.query(models.Users).filter(models.Users.id == user.get("id")).first()

        user_model.address_id = address_model.id

        db.add(user_model)
        db.commit()

        return f"Successfully entered the address for Username: {user_model.username}"
    else:
        return "Already filled"

