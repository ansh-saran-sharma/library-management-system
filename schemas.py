# Imports
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Literal

class Book(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    author: str
    status: Literal["AVAILABLE", "BORROWED"]
    price: float
    publisher: str
    page_count: int
    debut_year: str
    added_on: datetime = Field(default_factory=datetime.now)

class BookOut(Book):
    pass 

class UpdateBook(BaseModel):
    title: str
    author: str
    price: float
    publisher: str
    page_count: int
    debut_year: str

class CreateUser(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    password: str
    role: Literal["Librarian", "Member"]
    created_at: datetime = Field(default_factory=datetime.now)

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: str

class UpdateUser(BaseModel):
    email: str
    password: str

class Login(UpdateUser):
    pass

class Token(BaseModel):
    access_token: str
    bearer: str

class TokenPayLoad(BaseModel):
    email: EmailStr
    role: str