-- Create users table
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    user_type     TEXT NOT NULL
);

-- Create books table
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    year    INTEGER NOT NULL,
    author  TEXT NOT NULL,
    UNIQUE (title, year)
);

-- Create borrows table
CREATE TABLE borrows (
    borrow_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    book_id     INTEGER NOT NULL,
    borrow_date TEXT NOT NULL,
    return_date TEXT,
    returned    BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);