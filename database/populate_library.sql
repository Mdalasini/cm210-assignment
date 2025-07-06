-- Insert sample users (mix of 'patron' and 'admin')
-- The unhashed password is 'password'
INSERT INTO users (username, password_hash, user_type) VALUES
('alice', '87c8d21353c66ae15b22243d29100605', 'patron'), 
('bob', '87c8d21353c66ae15b22243d29100605', 'patron'),
('charlie', '87c8d21353c66ae15b22243d29100605', 'admin'),
('diana', '87c8d21353c66ae15b22243d29100605', 'patron'),
('eve', '87c8d21353c66ae15b22243d29100605', 'admin');

-- Insert sample books
INSERT INTO books (title, year, author) VALUES
('The Great Gatsby', 1925, 'F. Scott Fitzgerald'),
('To Kill a Mockingbird', 1960, 'Harper Lee'),
('1984', 1949, 'George Orwell'),
('Pride and Prejudice', 1813, 'Jane Austen'),
('Moby Dick', 1851, 'Herman Melville'),
('The Catcher in the Rye', 1951, 'J.D. Salinger'),
('Animal Farm', 1945, 'George Orwell'),
('Brave New World', 1932, 'Aldous Huxley');

-- Insert sample borrow records (only patrons can borrow)
-- Borrowed by alice (user_id = 1)
INSERT INTO borrows (user_id, book_id, borrow_date, return_date, returned) VALUES
(1, 1, '2024-01-10', '2024-01-20', TRUE),   -- Returned
(1, 2, '2024-02-01', NULL, FALSE);          -- Not returned

-- Borrowed by bob (user_id = 2)
INSERT INTO borrows (user_id, book_id, borrow_date, return_date, returned) VALUES
(2, 3, '2024-01-15', '2024-01-25', TRUE),
(2, 4, '2024-03-01', NULL, FALSE);

-- Borrowed by diana (user_id = 4)
INSERT INTO borrows (user_id, book_id, borrow_date, return_date, returned) VALUES
(4, 5, '2024-02-10', NULL, FALSE),
(4, 6, '2024-02-12', '2024-02-18', TRUE);