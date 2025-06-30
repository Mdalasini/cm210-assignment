from ..db.connection import get_connection
from ..models.models import UserCredentials, UserSummary, NewUser
from sqlite3 import Connection
from ..utils.hash import hash
from ..utils.defer import defer


class UserService:
    VALID_TYPES = {"patron", "admin"}

    @staticmethod
    def get_user_summary(user: UserCredentials) -> UserSummary | None:
        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            hashed = hash(user.password.strip())
            cursor.execute(
                "SELECT user_id, user_type FROM users WHERE username = ? AND password_hash = ?",
                (user.username.strip(), hashed),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            else:
                return UserSummary(*row)

    @staticmethod
    def username_exists(username: str) -> bool:
        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute(
                "SELECT 1 FROM users WHERE username = ?", (username.strip(),)
            )
            return cursor.fetchone() is not None

    @staticmethod
    def userid_exists(user_id: int) -> bool:
        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
            return cursor.fetchone() is not None

    @staticmethod
    def get_user_id(username: str) -> int | None:
        conn = get_connection()
        with defer(conn.cursor()) as cursor:
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            return cursor.fetchone()

    @staticmethod
    def new_user(new_user: NewUser) -> UserSummary:
        if new_user.user_type.strip() not in UserService.VALID_TYPES:
            raise ValueError("Invalid user_type. Must be 'patron' or 'admin'.")

        if UserService.username_exists(new_user.username):
            raise ValueError("Username already exists")

        conn = get_connection()
        with defer(conn.cursor()) as cursor:

            hashed = hash(new_user.password.strip())
            cursor.execute(
                "INSERT INTO users (username, password_hash, user_type) VALUES (?, ?, ?)",
                (new_user.username.strip(), hashed, new_user.user_type.strip()),
            )
            conn.commit()

            user_id = cursor.lastrowid

            return UserSummary(user_id, new_user.user_type)
