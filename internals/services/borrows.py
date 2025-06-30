from typing import List
from datetime import datetime
from ..models.models import BorrowSummary, BorrowRecord, NewBorrow
from ..db.connection import get_connection
from ..services.users import UserService
from ..services.books import BookService
from ..utils.defer import defer


class BorrowService:

    @staticmethod
    def get_all() -> List[BorrowSummary]:
        conn = get_connection()
        borrows: List[BorrowSummary] = []

        with defer(conn.cursor()) as cursor:
            cursor.execute("SELECT borrow_id, borrow_date, returned FROM borrows")
            rows = cursor.fetchall()
            for row in rows:
                borrow = BorrowSummary(*row)
                borrows.append(borrow)
            return borrows

    @staticmethod
    def get_users(user_id: int) -> List[BorrowRecord]:
        if not UserService.userid_exists(user_id):
            raise ValueError("User does not exist")

        conn = get_connection()
        borrows: List[BorrowRecord] = []

        with defer(conn.cursor()) as cursor:
            cursor.execute(
                "SELECT b.borrow_id, bk.title, bk.year, b.borrow_date, b.return_date, b.returned FROM borrows b JOIN books bk ON b.book_id = bk.book_id WHERE b.user_id = ?",
                (user_id,),
            )
            rows = cursor.fetchall()
            for row in rows:
                borrow = BorrowRecord(*row)
                borrows.append(borrow)
            return borrows

    @staticmethod
    def new_borrow(new_borrow: NewBorrow, user_id: int):
        book_id = BookService.get_book_id(new_borrow.book_title, new_borrow.book_year)

        if not book_id:
            raise ValueError("Book does not exist")
        elif not UserService.userid_exists(user_id):
            raise ValueError("User does not exist")

        today = datetime.now().date().isoformat()  # (YYYY-MM-DD)

        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO borrows (user_id, book_id, borrow_date, return_date, returned) VALUES (?, ?, ?, ?, ?)",
                (user_id[0], book_id[0], today, None, False),
            )
            conn.commit()

    @staticmethod
    def borrow_exists(borrow_id: int) -> bool:
        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute(
                "SELECT 1 FROM borrows WHERE borrow_id = ? LIMIT 1", (borrow_id,)
            )
            return cursor.fetchone() is not None

    @staticmethod
    def new_return(borrow_id: int, user_id: int):
        if not UserService.userid_exists(user_id):
            raise ValueError("User does not exist")

        today = datetime.now().date().isoformat()

        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute(
                "UPDATE borrows SET return_date = ?, returned = ? WHERE borrow_id = ? AND user_id = ?",
                (today, True, borrow_id, user_id),
            )
            conn.commit()
