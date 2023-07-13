import tkinter as tk 
from tkinter import messagebox
from library_database import LibraryDatabase

class LibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the window properties
        self.title("Library Database")
        self.geometry("800x600")  # Set the window size to 800x600

        # Initialize the library database
        self.library_db = LibraryDatabase()

        # Call methods to set up the GUI components
        self.create_menu()
        self.create_widgets()
        self.library_db.sort_database_title(self.book_listbox, "ASC")

    def create_menu(self):
        # Create the menu bar
        menubar = tk.Menu(self)

        # Create the File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
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

        # Create the frame for the search bar
        search_frame = tk.Frame(self)
        search_frame.grid(row=0, column=0, sticky="e", padx=10, pady=10)

        # submenu for exporting (csv)
        export_menu = tk.Menu(menubar, tearoff=0)
        export_menu.add_command(label="CSV", command=self.library_db.export_database_csv)

        menubar.add_cascade(label="Export", menu=export_menu)

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
        # Create and configure GUI components (labels, buttons, etc.)
        self.book_listbox = tk.Listbox(self, font=("Arial", 12), height=25, width=85)
        self.book_listbox.grid(row=1, column=0, padx=10, pady=10)

    def open_file(self):
        pass

    def save_file(self):
        pass

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

    def prompt_remove_book(self):
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

        # Perform the search operation based on the query
        # ...

# Create an instance of the LibraryGUI class and run the GUI
library_gui = LibraryGUI()
library_gui.mainloop()
