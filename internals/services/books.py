from typing import List
from ..models.models import BookSummary, NewBook
from ..db.connection import get_connection
from ..utils.defer import defer


class BookService:

    @staticmethod
    def get_all() -> List[BookSummary]:
        conn = get_connection()
        books: List[BookSummary] = []

        with defer(conn.cursor()) as cursor:
            cursor.execute("SELECT book_id, title, year, author FROM books")
            rows = cursor.fetchall()
            for row in rows:
                book = BookSummary(*row)
                books.append(book)
            return books

    @staticmethod
    def get_book_id(title: str, year: int) -> int | None:
        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute(
                "SELECT book_id FROM books WHERE title = ? AND year = ?",
                (title.strip(), year),
            )
            return cursor.fetchone()

    @staticmethod
    def book_exists(title: str, year: int) -> bool:
        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute(
                "SELECT 1 FROM books WHERE title = ? AND year = ?",
                (title.strip(), year),
            )
            return cursor.fetchone() is not None

    @staticmethod
    def new_book(new_book: NewBook):
        if BookService.book_exists(new_book.title, new_book.year):
            raise ValueError("Book already exists")

        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO books (title, year, author) VALUES (?, ?, ?)",
                (new_book.title, new_book.year, new_book.author),
            )
            conn.commit()
