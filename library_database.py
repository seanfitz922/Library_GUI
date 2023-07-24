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
            if len(str(int(pub_date))) > 4:
                raise ValueError("Publication date must be a valid number.")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Publication date must be a valid number.")
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

    def create_new_file(self, book_listbox, filepath):
        if filepath:
            # Create a new CSV file with the specified example book as the first line
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)

            # Show a message indicating the successful creation of the new file
            messagebox.showinfo("New File Created", f"New file '{os.path.basename(filepath)}' created.")

            # Update the current_file attribute to the newly created file
            self.current_file = filepath
            # Open the newly created file
            self.open_file(book_listbox, filepath)

    def open_file(self, book_listbox, file_path=None):
        if not file_path:
            # Open file browser dialog to select the file to open
            file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if file_path:
            # Clear the book_listbox before inserting results
            book_listbox.delete(0, tk.END)

            encodings_to_try = ['utf-8', 'utf-16', 'latin-1']

            for encoding in encodings_to_try:
                try:
                    # Open the CSV file using the current encoding
                    with open(file_path, newline='', encoding=encoding) as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            book_id = row['Book ID']
                            title = row['Title']
                            author = row['Author']
                            pub_date = row['Publication Date']
                            book_info = f"ID: {book_id} | Title: {title} | Author: {author} | Publication Date: {pub_date}"
                            book_listbox.insert(tk.END, book_info)
                            book_listbox.insert(tk.END, "")

                    # Update the current_file attribute to the newly opened file
                    self.current_file = file_path
                    print(str(file_path))
                    # Update the title label to show the current file
                    # self.update_title()

                    # Now, update the database with the contents of the opened CSV file
                    self.update_database_from_csv(file_path)
                    print(str(file_path))
                    # If the loop completes without errors, break out of the loop
                    break

                except Exception as e:
                    # If an error occurs, try the next encoding in the list
                    # *This throws several errors. Please ignore
                    print(str(e))
                    continue

        else:
            # If all encodings fail, show an error message
            messagebox.showerror("Error", "Failed to open the file with any of the supported encodings.")

    def update_database_from_csv(self, file_path):
        # Clear the current database to load the data from the CSV file
        self.cursor.execute("DELETE FROM books")

        try:
            # Open the CSV file using utf-8-sig encoding to handle BOM (Byte Order Mark)
            with open(file_path, newline='', encoding='utf-8', errors='replace') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book_id = row['Book ID']
                    title = row['Title']
                    author = row['Author']
                    pub_date = row['Publication Date']

                    # Insert the data from the CSV file into the database
                    self.cursor.execute("INSERT INTO books (book_id, title, author, pub_date) VALUES (?, ?, ?, ?)",
                                        (book_id, title, author, pub_date))

            # Commit the changes to the database
            self.conn.commit()

        except Exception as e:
            print(str(e))
            

    def save_file(self):
        if self.current_file:
            # Export the selected books to a temporary CSV file
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
                with open(filepath, 'w', newline='', encoding='utf-8') as file:
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
