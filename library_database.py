import sqlite3
from book_class import Book

class LibraryDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('library.db')  # Connect to the database
        self.cursor = self.conn.cursor()  # Create a cursor object
        self.create_books_table()  # Create the books table if it doesn't exist

    def create_books_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                pub_date INTEGER
            )
        ''')  # Create the books table with the specified columns
        self.conn.commit()  # Commit the changes to the database

    def add_book(self, book):
        self.cursor.execute('''
            INSERT INTO books (book_id, title, author, pub_date)
            VALUES (?, ?, ?, ?)
        ''', (book.book_id, book.title, book.author, book.pub_date))  # Insert a book into the books table
        self.conn.commit()  # Commit the changes to the database

    @staticmethod
    def print_all_books():
        conn = sqlite3.connect('library.db')  # Connect to the database
        cursor = conn.cursor()  # Create a cursor object

        cursor.execute("SELECT * FROM books")  # Execute the SQL query to retrieve all books
        rows = cursor.fetchall()  # Fetch all rows returned by the query

        if rows:
            for row in rows:
                book_id, title, author, pub_date = row
                print(f"Book ID: {book_id}, Title: {title}, Author: {author}, Publication Date: {pub_date}")
                # Print the book details
        else:
            print("No books found in the database.")  # Print a message if no books are found

        conn.close()  # Close the database connection

    def close_connection(self):
        self.conn.close()  # Close the database connection
