from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# SO, we have made a one-to-many relationship here, So, make Users the Parent Table & Todos the Child Table.
# Here Users can have multiple todos

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)

    at_todos = relationship("Todos", back_populates="at_owner",cascade="all, delete-orphan")
    address = relationship("Address", back_populates="user_address")


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    at_owner = relationship("Users", back_populates="at_todos")  # attribute_owner


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    postalcode = Column(String)
    country = Column(String)
    apt_number=Column(String)

    user_address = relationship("Users", back_populates="address")
