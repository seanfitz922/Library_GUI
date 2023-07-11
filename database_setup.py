import tkinter as tk
import sqlite3
from book_class import Book

class LibraryDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        self.create_books_table()

    def create_books_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                pub_date INTEGER
            )
        ''')
        self.conn.commit()

    def add_book(self, book):
        self.cursor.execute('''
            INSERT INTO books (book_id, title, author, pub_date)
            VALUES (?, ?, ?, ?)
        ''', (book.book_id, book.title, book.author, book.pub_date))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


