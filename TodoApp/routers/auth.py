# JWT is not an authentication method (i.e. basic & digest) but authorization method.
import sys

sys.path.append("..")

from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import Optional
from starlette import status
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "SECRETKEY_DSP"
ALGORITHM = "HS256"


# password for usename alpha is deepak1234

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone_number: Optional[str]


# for pass hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"Users": "Not Authorized"}}
)


# get_db function which gets the local session for manipulation in db.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# for pass hashing
def get_password_hash(password):
    return bcrypt_context.hash(password)


# user authentication step-1
def verify_password(plain_pass, hashed_pass):
    return bcrypt_context.verify(plain_pass, hashed_pass)


# user authentication step-2
def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# for token method
def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.get("/")
async def read_pass(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


# creating user database
@router.post("/create-users")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.phone_number = create_user.phone_number

    hash_password = get_password_hash(create_user.password)
    create_user_model.hashed_password = hash_password

    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Successful!'
    }


# creting funtion for access token back to the client
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    return {"token": token}


# decoding JWT token
async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}

    except JWTError:
        raise get_user_exception()


# Exceptions:
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect Username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response
