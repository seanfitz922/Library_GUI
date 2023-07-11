import tkinter as tk
import sqlite3
from book_class import Book
from library_database import LibraryDatabase

if __name__ == "__main__":
    # Create an instance of the LibraryDatabase class
    library_db = LibraryDatabase()

    # Create book objects and add them to the database
    book1 = Book(1, "The Great Gatsby", "F. Scott Fitzgerald", 1925)
    book2 = Book(2, "To Kill a Mockingbird", "Harper Lee", 1960)
    book3 = Book(3, "1984", "George Orwell", 1949)

    #library_db.add_book(book2)

    library_db.print_all_books()
    print()
    
    #library_db.remove_book(2)

    # Close the database connection
    library_db.close_connection()