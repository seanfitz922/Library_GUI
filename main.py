import tkinter as tk
import sqlite3
from book_class import Book
from library_database import LibraryDatabase

if __name__ == "__main__":
    # Create an instance of the LibraryDatabase class
    library_db = LibraryDatabase()

    # Create book objects and add them to the database
    
    #library_db.add_book(book2)

    library_db.sort_database_int("book_id")

    print()

    # Close the database connection
    library_db.close_connection()