import sqlite3, csv
from book_class import Book

class LibraryDatabase:
    def __init__(self):
        # Connect to the database
        self.conn = sqlite3.connect('library.db') 
        # Create a cursor object 
        self.cursor = self.conn.cursor() 
        # Create the books table if it doesn't exist 
        self.create_books_table()  

    def create_books_table(self):
        # Create the books table with the specified columns
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                pub_date INTEGER
            )
        ''')  
        # Commit the changes to the database
        self.conn.commit()  

    def add_book(self, book):
        # Insert a book into the books table
        self.cursor.execute('''
            INSERT INTO books (book_id, title, author, pub_date)
            VALUES (?, ?, ?, ?)
        ''', (book.book_id, book.title, book.author, book.pub_date))  
        # Commit the changes to the database
        self.conn.commit()  

    def remove_book(self, book_id):
        # Remove book from table with book id
        self.cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,)) 
        self.conn.commit()

    def query_by_col(self, column):
        # Validate the column input
        valid_columns = ["book_id", "title", "author", "pub_date"]
        if column not in valid_columns:
            print("Invalid column name. Please enter a valid column: book_id, title, author, or pub_date")
            return

        # Execute the SQL query to select the specified column from the books table
        self.cursor.execute(f"SELECT {column} FROM books")
        rows = self.cursor.fetchall()

        if rows:
            # Extract the values from the result rows
            column_values = [row[0] for row in rows]
            # Print the column values
            print(f"All {column} values:")
            for value in column_values:
                print(value)
        else:
            print("No books found in the database.")

    @staticmethod
    def print_all_books():
        # Connect to the database
        conn = sqlite3.connect('library.db')  
        # Create a cursor object
        cursor = conn.cursor()  

        # Execute the SQL query to retrieve all books
        cursor.execute("SELECT * FROM books")  
        # Fetch all rows returned by the query
        rows = cursor.fetchall()  

        if rows:
            for row in rows:
                book_id, title, author, pub_date = row
                print(f"Book ID: {book_id}, Title: {title}, Author: {author}, Publication Date: {pub_date}")
                # Print the book details
        else:
            # Print a message if no books are found
            print("No books found in the database.")  

        # Close the database connection
        conn.close()  

    def sort_database_title(self):
        # Execute the SQL query to select the book titles from the books table
        self.cursor.execute("SELECT title FROM books")
        rows = self.cursor.fetchall()

        if rows:
            # Extract the book titles from the result rows
            book_titles = [row[0] for row in rows]

            # Define a custom sorting key function
            def sort_key(title):
                # Split the title into words
                words = title.split()
                # Ignore certain words at the beginning
                if len(words) > 1 and words[0].lower() in ["the", "a", "an"]:
                    # Sort based on the second word
                    return words[1]  
                else:
                    # Sort as is
                    return title  

            # Sort the book titles using the custom sorting key function
            sorted_titles = sorted(book_titles, key=sort_key)

            return sorted_titles

            # Print the sorted book titles
            """
            print("Book Titles (Alphabetical Order):")
            for title in sorted_titles:
                print(title)
        else:
            print("No books found in the database.")
            """

    def sort_database_int(self, column):
        # Validate the column input
        valid_columns = ["book_id", "pub_date"]
        if column not in valid_columns:
            print("Invalid column name. Please enter a valid column: book_id or pub_date")
            return

        # Execute the SQL query to select all columns from the books table and order by the specified column in ascending order
        self.cursor.execute(f"SELECT * FROM books ORDER BY {column} ASC")
        rows = self.cursor.fetchall()

        if rows:
            # Print the sorted results
            print(f"Sorted Database (Ascending Order - {column}):")
            for row in rows:
                row_str = ", ".join(str(value) for value in row)
                print(row_str)
        else:
            print("No books found in the database.")

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
