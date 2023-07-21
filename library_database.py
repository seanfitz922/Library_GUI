import sqlite3, csv, os
import tkinter as tk
from book_class import Book
from tkinter import messagebox, filedialog


class LibraryDatabase:
    def __init__(self, parent):
        
        self.parent = parent
        self.current_file = None
        # Connect to the database
        self.conn = sqlite3.connect('library.db') 
        # Create a cursor object 
        self.cursor = self.conn.cursor() 
        # Create the books table if it doesn't exist 
        self.create_books_table()  
        
        #self.fill_db()

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

    def populate_books(self, columns, book_listbox):
        # Clear the book_listbox before inserting results
        book_listbox.delete(0, tk.END)

        # Display books
        for column in columns:
            # Format the book information
            book_info = f"ID: {column[0]} | Title: {column[1]} | Author: {column[2]} | Publication Date: {column[3]}"

            # Insert the formatted book information into the book_listbox
            book_listbox.insert(tk.END, book_info)
            book_listbox.insert(tk.END, "")


    def add_book(self, title, author, pub_date, popup_window, book_listbox):
        # Validate the input
        if not title or not author or not pub_date:
            messagebox.showwarning("Invalid Input", "Please provide all book details.")
            return
        
        # Check if pub_date is a valid four-digit number
        try:
            if len(str(int(pub_date))) != 4:
                raise ValueError("Publication date must be a valid four-digit number.")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Publication date must be a valid four-digit number.")
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

        book_listbox.insert(tk.END, f"ID: {book_id} | Title: {title} | Author: {author} | Publication Date: {pub_date}")
        messagebox.showinfo("Success", "Book added successfully.")
        
        popup_window.destroy()
        popup_window.grab_release()

    def get_max_book_id(self):
        self.cursor.execute("SELECT MAX(book_id) FROM books")
        max_id = self.cursor.fetchone()[0]
        return max_id if max_id is not None else 0

    def remove_book(self, book_id, popup_window, book_listbox):
        # Remove book from table with book id
        if not book_id:
            messagebox.showwarning("Invalid Input", "Please provide the book's ID.")
            return

        # Execute the SQL query to fetch the book with the provided book ID
        self.cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        book = self.cursor.fetchone()

        # Check if the book ID exists in the database
        if not book:
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
        popup_window.grab_release()


    def sort_database_title(self, book_listbox, order):
        # Execute the SQL query to select all columns from the books table
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()

        if rows:
            # Define a custom sorting key function
            def sort_key(row):
                # Extract the title from the row
                title = row[1]
                # Split the title into words
                words = title.split()
                # Ignore certain words at the beginning
                if len(words) > 1 and words[0].lower() in ["the", "a", "an"]:
                    # Sort based on the second word
                    return words[1]
                else:
                    # Sort as is
                    return title

            if order == "ASC":
                # Sort the rows based on the custom sorting key function
                sorted_rows = sorted(rows, key=sort_key)
            else:
                # Sort the rows based on the custom sorting key function in descending order
                sorted_rows = sorted(rows, key=sort_key, reverse=True)

            self.populate_books(sorted_rows, book_listbox)

    def sort_database_author(self, book_listbox, order):
        self.cursor.execute(f"SELECT * FROM books ORDER BY author {order}")
        rows = self.cursor.fetchall()

        if rows:
            self.populate_books(rows, book_listbox)

    def sort_database_int(self, column, book_listbox, order):
        # Execute the SQL query to select all columns from the books table and order by the publication date in ascending order
        self.cursor.execute(f"SELECT * FROM books ORDER BY {column} {order}")
        rows = self.cursor.fetchall()

        if rows:
            self.populate_books(rows, book_listbox)

    def close_file(self):
        # Close the current window
        self.parent.destroy()

    def open_file(self, book_listbox):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.current_file = file_path

            # Clear the current database
            self.cursor.execute("DELETE FROM books")
            self.conn.commit()

            # Read the CSV file and populate the database
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    book_id_str = row['Book ID']
                    title = row['Title']
                    author = row['Author']
                    pub_date_str = row['Publication Date']

                    try:
                        # Convert book_id and pub_date to integers
                        book_id = int(book_id_str) if book_id_str else None
                        pub_date = int(pub_date_str) if pub_date_str else None
                    except ValueError:
                        # If the conversion fails, skip this row and continue with the next one
                        continue

                    self.cursor.execute('''
                        INSERT INTO books (book_id, title, author, pub_date)
                        VALUES (?, ?, ?, ?)
                    ''', (book_id, title, author, pub_date))
            self.conn.commit()
            # Fetch all rows from the database
            self.cursor.execute("SELECT * FROM books")
            rows = self.cursor.fetchall()

            # Update the book_listbox with the new data
            self.populate_books(rows, book_listbox)

    def save_file(self):
        if self.current_file:
            # Export the current database to a temporary CSV file
            temp_file = "temp_library_database.csv"
            with open(temp_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Book ID', 'Title', 'Author', 'Publication Date'])

                self.cursor.execute("SELECT * FROM books")
                rows = self.cursor.fetchall()

                for row in rows:
                    writer.writerow(row)

            # Replace the original CSV file with the temporary file
            os.replace(temp_file, self.current_file)

            messagebox.showinfo("Success", "Changes saved successfully.")
        else:
            messagebox.showwarning("Save Failed", "No file is currently open. Please open a CSV file before saving changes.")

    def export_database_csv(self):
        # Open file browser dialog to select the save location
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

        # Check if a file was selected
        if filepath:
            # Execute SQL query to select all rows from the books table
            self.cursor.execute("SELECT * FROM books")
            rows = self.cursor.fetchall()

            if rows:
                # Open the CSV file at the selected location in write mode
                with open(filepath, 'w', newline='') as file:
                    # Create a CSV writer object
                    writer = csv.writer(file)
                    # Write the column headers to the CSV file
                    writer.writerow(['Book ID', 'Title', 'Author', 'Publication Date'])
                    # Write all the rows to the CSV file
                    writer.writerows(rows)
                    
                messagebox.showinfo("Export Success", "Library database exported to " + filepath)
            else:
                messagebox.showwarning("Export Failed", "No books found in the database.")
        else:
            messagebox.showwarning("Export Cancelled", "No file selected.")
    
    

    def close_connection(self):
        self.conn.close()  # Close the database connection

    def search_books(self, search_query):
        # Execute the SQL query to search for books matching the query
        self.cursor.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR book_id LIKE ? OR pub_date LIKE ?",
            ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%')
        )
        rows = self.cursor.fetchall()

        # Return the search results
        return rows


"""
    def fill_db(self):
        for book_data in books_data:
            book = Book(book_data["book_id"], book_data["title"], book_data["author"], book_data["pub_date"])
            self.add_books_db(book)


    def add_books_db(self, book):
        self.cursor.execute('''
            INSERT INTO books (book_id, title, author, pub_date)
            VALUES (?, ?, ?, ?)
        ''', (book.book_id, book.title, book.author, book.pub_date))
        self.conn.commit()

        print(f"Book added to the database: {book.title} by {book.author} ({book.pub_date})")
"""
