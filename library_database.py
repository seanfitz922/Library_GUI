import sqlite3, csv
from book_class import Book
import tkinter as tk
from tkinter import messagebox


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

    def add_book(self, title, author, pub_date, popup_window, book_listbox):
        # Validate the input
        if not title or not author or not pub_date:
            messagebox.showwarning("Invalid Input", "Please provide all book details.")
            return

        # Get the current maximum book_id from the database
        max_book_id = self.get_max_book_id()

        # Calculate the new book_id by incrementing the maximum book_id by 1
        book_id = max_book_id + 1

        # Insert the book into the library database
        self.cursor.execute('''
            INSERT INTO books (book_id, title, author, pub_date)
            VALUES (?, ?, ?, ?)
        ''', (book_id, title, author, pub_date))
        self.conn.commit()

        book_listbox.insert(tk.END, f"{book_id}: {title} by {author} ({pub_date})")
        messagebox.showinfo("Success", "Book added successfully.")
        popup_window.destroy()

    def get_max_book_id(self):
        self.cursor.execute("SELECT MAX(book_id) FROM books")
        max_id = self.cursor.fetchone()[0]
        return max_id if max_id is not None else 0

    def remove_book(self, book_id, popup_window, book_listbox):
        # Remove book from table with book id
        if not book_id:
            messagebox.showwarning("Invalid Input", "Please provide the book's ID.")
            return
        
        # Check if the book ID exists in the database
        if self.cursor.fetchone() is None:
            messagebox.showwarning("Invalid Book ID", "The provided book ID does not exist.")
            return

        self.cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,)) 
        self.conn.commit()

        # Remove book from the book_listbox
        selected_indices = book_listbox.curselection()
        if selected_indices:
            book_listbox.delete(selected_indices[0])

        messagebox.showinfo("Success", "Book removed successfully.")
        popup_window.destroy()

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

    def sort_database_title(self, book_listbox):
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

            # Clear the book_listbox before inserting the sorted results
            book_listbox.delete(0, tk.END)

            # Display the sorted results
            for title in sorted_titles:
                book_listbox.insert(tk.END, title)

        

    def sort_database_int(self, column, book_listbox):
        # Execute the SQL query to select all columns from the books table and order by the publication date in ascending order
        self.cursor.execute(f"SELECT * FROM books ORDER BY {column} ASC")
        rows = self.cursor.fetchall()

        if rows:
            # Clear the book_listbox before inserting the sorted results
            book_listbox.delete(0, tk.END)

            # Display the sorted results
            for row in rows:
                book_listbox.insert(tk.END, row)

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
