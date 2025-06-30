# Library Management System API

This repository contains the API for the Library Management System being developed as part of the **CMT 210** group assignment.

---

## 🔗 Endpoints

### Authentication

* `POST /login`

  * Accepts: `{ username, password }`
  * Returns: a session token if the credentials are valid

### Books

* `GET /all/books`

  * Returns: a JSON array of books with fields `[book_id, title, year, author]`

### Borrows

* `GET /all/borrows`

  * Returns: a JSON array of borrows with fields `[borrow_id, borrow_date, returned]`

* `GET /user/borrows`

  * Parameters: `id` (representing `user_id`)
  * Returns: all borrows for a specific user with fields `[borrow_id, title, year, borrow_date, return_date, returned]`

### Users

* `POST /new/user`

  * Accepts: `{ username, password, user_type ('patron' or 'admin') }`
  * Returns: a session token

### Admin/Patron Actions *(currently disabled)*

* `POST /new/book`

  * Accepts: `{ title, year, author }`
  * Requires: admin access (currently disabled)
  * Action: Adds a new book to the database

* `POST /new/borrow`

  * Accepts: `{ book_title, book_year }`
  * Requires: patron access (currently disabled, uses hardcoded `user_id = 1`)
  * Action: Adds a new borrow entry

* `POST /new/return`

  * Parameters: `id` (representing `borrow_id`)
  * Requires: patron access (currently disabled, uses hardcoded `user_id = 1`)
  * Action: Marks a borrow as returned and sets `return_date` to today

---

## 📁 Setup Instructions

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create the database**

   From the project root:

   ```bash
   sqlite3 database/library.db < database/create_library.sql
   sqlite3 database/library.db < database/populate_library.sql
   ```

---

## ⚠️ Notes

* The file `database/library.db` should **not** be tracked in version control.
* Database structure and sample data can be recreated using the SQL scripts provided.
* Some endpoints are currently hardcoded or disabled and are intended for future improvement.
