DROP TABLE IF EXISTS books;
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    publisher TEXT,
    publication_date TEXT,
    genre TEXT,
    status TEXT,
    rating TEXT,
    memo TEXT
);