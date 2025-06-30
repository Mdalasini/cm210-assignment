from dataclasses import dataclass
from datetime import date
from pydantic import BaseModel
from typing import Optional

# -- Summary Models (read/display)

@dataclass
class BookSummary:
    book_id: int
    title: str
    year: int
    author: str

@dataclass
class BorrowSummary:
    borrow_id: int
    borrow_date: str
    returned: bool

@dataclass
class BorrowRecord:
    borrow_id: int
    title: str
    year: int
    borrow_date: str
    return_date: Optional[str]
    returned: bool

@dataclass
class UserSummary:
    user_id: int
    user_type: str

# -- Input Models (write/insert)

class UserCredentials(BaseModel):
    username: str
    password: str # unhashed

class NewUser(BaseModel):
    username: str
    password: str  # unhashed before storage
    user_type: str  # should be 'patron' or 'admin'

class NewBook(BaseModel):
    title: str
    year: int
    author: str

class NewBorrow(BaseModel):
    book_title: str
    book_year: int

class NewReturn(BaseModel):
    borrow_id: int
