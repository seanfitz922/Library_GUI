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
        self.populate_book_list()

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
        actions_menu.add_command(label="Add", command=self.add_book)
        actions_menu.add_command(label="Remove", command=self.remove_book)
        menubar.add_cascade(label="Actions", menu=actions_menu)

        # Create the Sort menu
        sort_menu = tk.Menu(menubar, tearoff=0)

        # submenu for title sorting
        sort_title_submenu = tk.Menu(sort_menu, tearoff=0)
        sort_title_submenu.add_command(label="A-Z", command=self.sort_by_title_ascending)
        sort_title_submenu.add_command(label="Z-A", command=self.sort_by_title_descending)
        sort_menu.add_cascade(label="Title", menu=sort_title_submenu)

        # submenu for author sorting
        sort_author_submenu = tk.Menu(sort_menu, tearoff=0)
        sort_author_submenu.add_command(label="A-Z", command=self.sort_by_author_ascending)
        sort_author_submenu.add_command(label="Z-A", command=self.sort_by_author_descending)
        sort_menu.add_cascade(label="Author", menu=sort_author_submenu)

        # submenu for publication date sorting
        sort_pubdate_submenu = tk.Menu(sort_menu, tearoff=0)
        sort_pubdate_submenu.add_command(label="Ascending", command=self.sort_by_pub_date_ascending)
        sort_pubdate_submenu.add_command(label="Descending", command=self.sort_by_pub_date_descending)
        sort_menu.add_cascade(label="Publication Date", menu=sort_pubdate_submenu)

        # submenu for book id sorting
        sort_id_submenu = tk.Menu(sort_menu, tearoff=0)
        sort_id_submenu.add_command(label="Ascending", command=self.sort_by_id_ascending)
        sort_id_submenu.add_command(label="Descending", command=self.sort_by_id_descending)
        sort_menu.add_cascade(label="ID", menu=sort_id_submenu)

        menubar.add_cascade(label="Sort", menu=sort_menu)

        # Configure the window to use the menu bar
        self.config(menu=menubar)

    def create_widgets(self):
        # Create and configure GUI components (labels, buttons, etc.)
        self.book_listbox = tk.Listbox(self, font=("Arial", 12), height=30, width = 100)
        self.book_listbox.grid(row=0, column=0)

    
    def populate_book_list(self):
        # Retrieve book titles from the library database and populate the listbox
        book_titles = self.library_db.sort_database_title()

        for title in book_titles:
            self.book_listbox.insert(tk.END, title)

    def open_file(self):
        pass

    def save_file(self):
        pass

    def add_book(self):
        pass

    def remove_book(self):
        pass

    def sort_by_title_ascending(self):
        pass

    def sort_by_title_descending(self):
        pass

    def sort_by_author_ascending(self):
        pass

    def sort_by_author_descending(self):
        pass

    def sort_by_id_ascending(self):
        pass

    def sort_by_id_descending(self):
        pass

    def sort_by_pub_date_ascending(self):
        pass

    def sort_by_pub_date_descending(self):
        pass
    
    def sort_pub_date(self):
        pass

# Create an instance of the LibraryGUI class and run the GUI
library_gui = LibraryGUI()
library_gui.mainloop()