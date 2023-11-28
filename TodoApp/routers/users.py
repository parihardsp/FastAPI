"""Recap what we have learned. We will be creating a new route that has a lot of functionality that we have learned thus far from FastAPI :)
    - Create a new route within the routers directory called users.py
    - Enhance users.py to be able to return all users within the application
    - Enhance users.py to be able to get a single user by a path parameter
    - Enhance users.py to be able to get a single user by a query parameter
    - Enhance users.py to be able to modify their current user's password, if passed by authentication
    - Enhance users.py to be able to delete their own user."""

import sys

sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from .auth import get_current_user, get_user_exception, verify_password, get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"Users": "Not Found"}}
)
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/{user_id}")
async def read_user_bypath(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is not None:
        return user_model
    return "Invalid User ID"


@router.get("/userID/")
async def read_user_byquery(userID: str, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == userID).first()
    if user_model is not None:
        return user_model
    return "Invalid User ID"



# @router.put("/ChangePassword/")
# async def user_password_change(user_verification=Depends(UserVerification),
#                                user: dict = Depends(get_current_user),
#                                db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#
#     user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
#
#     if user_model is not None:
#         if user_verification.username == user_model.username and \
#                 verify_password(user_verification.password, user_model.hashed_password):
#             user_model.hashed_password = get_password_hash(user_verification.new_password)
#             db.add(user_model)
#             db.commit()
#             return "Successfull Updation"
#     return "Invalid User or Request"

@router.put("/ChangePassword/")
async def user_password_change(
    user_verification: UserVerification,  # Use the UserVerification model directly
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is not None:
        if (
            user_verification.username == user_model.username
            and verify_password(user_verification.password, user_model.hashed_password)
        ):
            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return "Successful Update"
    return "Invalid User or Request"


@router.delete("/delete")
async def delete_user(user: dict =Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None:
        return "Invalid User or Request"

    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()

    db.commit()

    return "Delete Successfull"
