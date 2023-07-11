import sqlite3, csv
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

    def remove_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,)) # Remove book from table with book id
        self.conn.commit()

    def query_by_col(self, book_col):
        # Validate the book_col input
        valid_columns = ["book_id", "title", "author", "pub_date"]
        if book_col not in valid_columns:
            print("Invalid column name. Please enter a valid column: book_id, title, author, or pub_date")
            return

        # Execute the SQL query to select the specified column from the books table
        self.cursor.execute(f"SELECT {book_col} FROM books")
        rows = self.cursor.fetchall()

        if rows:
            # Extract the values from the result rows
            column_values = [row[0] for row in rows]
            # Print the column values
            print(f"All {book_col} values:")
            for value in column_values:
                print(value)
        else:
            print("No books found in the database.")

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

    def export_database_csv(self):
    # Execute SQL query to select all rows from the books table
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()

        if rows:
            # Open the CSV file in write mode
            with open('library_database.csv', 'w', newline='') as file:
                # Create a CSV writer object
                writer = csv.writer(file)
                # Write the column headers to the CSV file
                writer.writerow(['Book ID', 'Title', 'Author', 'Publication Date'])
                # Write all the rows to the CSV file
                writer.writerows(rows)
            print("Library database exported to library_database.csv")
        else:
            print("No books found in the database.")


    def close_connection(self):
        self.conn.close()  # Close the database connection
