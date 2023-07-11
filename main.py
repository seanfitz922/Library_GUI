import tkinter as tk
import sqlite3
from book_class import Book
from library_database import LibraryDatabase

if __name__ == "__main__":
    # Create an instance of the LibraryDatabase class
    library_db = LibraryDatabase()
    
    # Close the database connection
    library_db.close_connection()