import tkinter as tk 
import os
from tkinter import messagebox, filedialog
from library_database import LibraryDatabase

class LibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set up the window properties
        self.title("Library Database")
        # Set the window size to 800x600
        self.geometry("800x600")  
        # Initialize the library database
        self.library_db = LibraryDatabase(self)
        # Define a variable to store the current file name
        # Call methods to set up the GUI components
        self.create_menu()
        self.create_widgets()
        # database is sorted by book_id everytime program is opened
        self.library_db.sort_database_int("book_id", self.book_listbox, "ASC")

    def create_menu(self):
        # Create the menu bar
        menubar = tk.Menu(self)

        # Create the File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.library_db.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Close", command=self.library_db.close_file)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create the Actions menu
        actions_menu = tk.Menu(menubar, tearoff=0)
        actions_menu.add_command(label="Add", command=self.prompt_add_book)
        actions_menu.add_command(label="Remove", command=self.prompt_remove_book)
        menubar.add_cascade(label="Actions", menu=actions_menu)

        # Create the Sort menu
        sort_menu = tk.Menu(menubar, tearoff=0)

        # submenu for title sorting
        sort_title_submenu = tk.Menu(sort_menu, tearoff=0)
        sort_title_submenu.add_command(label="A-Z", command=lambda: self.library_db.sort_database_title(self.book_listbox, "ASC"))
        sort_title_submenu.add_command(label="Z-A", command=lambda: self.library_db.sort_database_title(self.book_listbox, "DESC"))
        sort_menu.add_cascade(label="Title", menu=sort_title_submenu)

        # submenu for author sorting
        sort_author_submenu = tk.Menu(sort_menu, tearoff=0)
        sort_author_submenu.add_command(label="A-Z", command=lambda: self.library_db.sort_database_author(self.book_listbox, "ASC"))
        sort_author_submenu.add_command(label="Z-A", command=lambda: self.library_db.sort_database_author(self.book_listbox, "DESC"))
        sort_menu.add_cascade(label="Author", menu=sort_author_submenu)

        # submenu for publication date sorting
        sort_pubdate_submenu = tk.Menu(sort_menu, tearoff=0)
        sort_pubdate_submenu.add_command(label="Ascending", command=lambda: self.library_db.sort_database_int("pub_date", self.book_listbox, "ASC"))
        sort_pubdate_submenu.add_command(label="Descending", command=lambda: self.library_db.sort_database_int("pub_date", self.book_listbox, "DESC"))
        sort_menu.add_cascade(label="Publication Date", menu=sort_pubdate_submenu)

        # submenu for book id sorting
        sort_id_submenu = tk.Menu(sort_menu, tearoff=0)
        sort_id_submenu.add_command(label="Ascending", command=lambda: self.library_db.sort_database_int("book_id", self.book_listbox, "ASC"))
        sort_id_submenu.add_command(label="Descending", command=lambda: self.library_db.sort_database_int("book_id", self.book_listbox, "DESC"))
        sort_menu.add_cascade(label="ID", menu=sort_id_submenu)

        menubar.add_cascade(label="Sort", menu=sort_menu)

        # submenu for exporting (csv)
        export_menu = tk.Menu(menubar, tearoff=0)
        export_menu.add_command(label="CSV", command=self.library_db.export_database_csv)

        menubar.add_cascade(label="Export", menu=export_menu)

         # Create the frame for the search bar
        search_frame = tk.Frame(self)
        search_frame.grid(row=0, column=0, sticky="e", padx=10, pady=10)

        # Create the Search bar
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, padx=5, sticky="e")
        search_entry.bind("<Return>", self.search_books)
        search_button = tk.Button(search_frame, text="Search", command=self.search_books)
        search_button.grid(row=0, column=1, padx=5, sticky="e")

        # Configure the window to use the menu bar
        self.config(menu=menubar)

    def create_widgets(self):
        # Label for the current file name
        self.file_label = tk.Label(self, text="Current File: ")
        self.file_label.grid(row=0, column=0, sticky="w")

        # Create and configure GUI components (listbox, buttons, etc.)
        self.book_listbox = tk.Listbox(self, font=("Arial", 12), height=25, width=85)
        self.book_listbox.grid(row=1, column=0, padx=10, pady=10)

       # Create a context menu
        self.context_menu = tk.Menu(self.book_listbox, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_book_details)
        self.context_menu.add_command(label="Remove", command=self.prompt_remove_book)

        # Bind the double-click event to show_book_details function
        self.book_listbox.bind("<Double-Button-1>", self.show_book_details)

        # Bind the left,right-click event to show the context menu
        self.book_listbox.bind("<Button-1>", self.on_book_click)
        self.book_listbox.bind("<Button-3>", self.show_context_menu)

    def on_book_click(self, event):
        # Get the selected book index from the event
        self.selected_book_index = self.book_listbox.nearest(event.y)

    def save_file(self):
        pass

    def edit_book(self):
        pass

    def show_context_menu(self, event):
        # Only display the context menu if a book is selected
        if self.selected_book_index is not None:
            # Display the context menu at the right-click location
            self.context_menu.post(event.x_root, event.y_root)

    def show_book_details(self, event):
        # Get the selected book index from the book_listbox
        selected_index = self.book_listbox.curselection()

        if selected_index:
            # Set the selected book index
            self.selected_book_index = selected_index

            # Call edit_book_details to show the details popup
            self.edit_book_details()

    def edit_book_details(self):
        # Get the selected book information from the listbox
        selected_book = self.book_listbox.get(self.selected_book_index)

        # Split the book information into separate fields (ID, Title, Author, Publication Date)
        book_id, title, author, pub_date = selected_book.split("|")

        # Extract only the values from the book information
        book_id = book_id.split(":")[1].strip()
        title = title.split(":")[1].strip()
        author = author.split(":")[1].strip()
        pub_date = pub_date.split(":")[1].strip()

        # Create a larger pop-up window
        details_popup = tk.Toplevel(self)
        details_popup.title("Book Details")

        # Set the size of the pop-up window
        details_popup.geometry("400x300")  # Adjust the width and height as needed

        # Create labels
        label_font = ("Arial", 12)  # Adjust the font family and size as needed
        id_label = tk.Label(details_popup, text="Book ID:", font=label_font)
        title_label = tk.Label(details_popup, text="Title:", font=label_font)
        author_label = tk.Label(details_popup, text="Author:", font=label_font)
        pub_date_label = tk.Label(details_popup, text="Publication Date:", font=label_font)

        # Create entry fields
        entry_font = ("Arial", 10)  # Adjust the font family and size as needed
        id_entry = tk.Entry(details_popup, width=30, font=entry_font)  # Adjust the width as needed
        title_entry = tk.Entry(details_popup, width=30, font=entry_font)  # Adjust the width as needed
        author_entry = tk.Entry(details_popup, width=30, font=entry_font)  # Adjust the width as needed
        pub_date_entry = tk.Entry(details_popup, width=30, font=entry_font)  # Adjust the width as needed

        # Set the initial values of the entry fields
        id_entry.insert(0, book_id)
        title_entry.insert(0, title)
        author_entry.insert(0, author)
        pub_date_entry.insert(0, pub_date)

        # Arrange the labels and entry fields using grid()
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry.grid(row=0, column=1, padx=10, pady=10)
        title_label.grid(row=1, column=0, padx=10, pady=10)
        title_entry.grid(row=1, column=1, padx=10, pady=10)
        author_label.grid(row=2, column=0, padx=10, pady=10)
        author_entry.grid(row=2, column=1, padx=10, pady=10)
        pub_date_label.grid(row=3, column=0, padx=10, pady=10)
        pub_date_entry.grid(row=3, column=1, padx=10, pady=10)

        # Function to handle the Submit Changes button click
        def submit_changes():
            # Get the updated values from the entry fields
            updated_book_id = id_entry.get()
            updated_book_title = title_entry.get()
            updated_pub_date = pub_date_entry.get()
            updated_author = author_entry.get()

            # Check if the updated book ID is changed
            if updated_book_id != book_id:
                # Check if the updated book ID is an integer
                try:
                    updated_book_id = int(updated_book_id)
                except ValueError:
                    messagebox.showerror("Invalid Book ID", "Book ID must be an integer.")
                    return

                # Check if the updated book ID is already in use
                self.library_db.cursor.execute("SELECT book_id FROM books WHERE book_id=?", (updated_book_id,))
                existing_book = self.library_db.cursor.fetchone()
                if existing_book:
                    messagebox.showerror("Duplicate Book ID", "Book ID is already in use. Please choose a different ID.")
                    return

            # Update the book information in the book_listbox
            updated_book_info = f"ID: {updated_book_id} | Title: {updated_book_title.strip()} | Author: {updated_author.strip()} | Publication Date: {updated_pub_date.strip()}"
            self.book_listbox.delete(self.selected_book_index)
            self.book_listbox.insert(self.selected_book_index, updated_book_info)

            # Update the book information in the database
            self.library_db.cursor.execute(
                "UPDATE books SET book_id=?, title=?, author=?, pub_date=? WHERE book_id=?",
                (updated_book_id, updated_book_title, updated_author, updated_pub_date, book_id)
            )
            self.library_db.conn.commit()

            # Destroy the pop-up window after editing
            details_popup.destroy()

            # When the pop-up is closed, release the grab
            details_popup.grab_release()

        # Create a Submit Changes button
        submit_button = tk.Button(details_popup, text="Submit Changes", command=submit_changes)
        submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Add these lines to make the popup appear in front and wait until closed
        details_popup.grab_set()
        details_popup.wait_window()

    def prompt_add_book(self):
        # Create a new popup window
        popup_window = tk.Toplevel(self)
        popup_window.title("Add Book")

        # Create labels and entry fields for book details
        title_label = tk.Label(popup_window, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        title_entry = tk.Entry(popup_window)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        author_label = tk.Label(popup_window, text="Author:")
        author_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        author_entry = tk.Entry(popup_window)
        author_entry.grid(row=1, column=1, padx=10, pady=5)

        pub_date_label = tk.Label(popup_window, text="Publication Date:")
        pub_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        pub_date_entry = tk.Entry(popup_window)
        pub_date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Create a button to confirm adding the book
        add_button = tk.Button(popup_window, text="Add", command=lambda: self.library_db.add_book(
            title_entry.get(), author_entry.get(), pub_date_entry.get(), popup_window, self.book_listbox))
        add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def prompt_remove_book(self, event=None):
        popup_window = tk.Toplevel(self)
        popup_window.title("Remove Book")

        # Create labels and entry fields for book ID
        id_label = tk.Label(popup_window, text="Book ID:")
        id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        id_entry = tk.Entry(popup_window)
        id_entry.grid(row=0, column=1, padx=10, pady=5)


        # Create a button to confirm removing the book
        remove_button = tk.Button(popup_window, text="Remove", command=lambda: self.library_db.remove_book(
            id_entry.get(), popup_window, self.book_listbox))
        remove_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def search_books(self, event=None):
        # Retrieve the search query from the search bar
        search_query = self.search_var.get()

        # Clear the book_listbox before performing the search
        self.book_listbox.delete(0, tk.END)

        # Perform the search operation based on the query
        results = self.library_db.search_books(search_query)
        if results:
            # Display the search results in the book_listbox

            for book in results:
                book_info = f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Publication Date: {book[3]}"
                self.book_listbox.insert(tk.END, book_info)
        else:
            messagebox.showinfo("No Results", "No books matching the search query found.")



# Create an instance of the LibraryGUI class and run the GUI
library_gui = LibraryGUI()
library_gui.mainloop()
