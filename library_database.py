import sqlite3, csv
from book_class import Book
import tkinter as tk
from tkinter import messagebox, filedialog


class LibraryDatabase:
    def __init__(self, parent):
        
        self.parent = parent
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

    def populate_books(self, column, book_listbox):
        # Clear the book_listbox before inserting results
        book_listbox.delete(0, tk.END)

        # Display books
        for columns in column:
                book_listbox.insert(tk.END, columns)

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

    def sort_database_title(self, book_listbox, order):
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

            if order == "ASC":
                # Sort the book titles using the custom sorting key function
                sorted_titles = sorted(book_titles, key=sort_key)
            else:
                # Sort the book using custom sorting key and in descending order
                sorted_titles = sorted(book_titles, key=sort_key, reverse=True)

            self.populate_books(sorted_titles, book_listbox)

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


    def fill_db(self):
        books_data = [
    {"book_id": 1, "title": "1984", "author": "George Orwell", "pub_date": 1949},
    {"book_id": 2, "title": "A Brief History of Time", "author": "Stephen Hawking", "pub_date": 1988},
    {"book_id": 3, "title": "A Farewell to Arms", "author": "Ernest Hemingway", "pub_date": 1929},
    {"book_id": 4, "title": "A Game of Thrones", "author": "George R.R. Martin", "pub_date": 1996},
    {"book_id": 5, "title": "A Passage to India", "author": "E.M. Forster", "pub_date": 1924},
    {"book_id": 6, "title": "A Tale of Two Cities", "author": "Charles Dickens", "pub_date": 1859},
    {"book_id": 7, "title": "Alice's Adventures in Wonderland", "author": "Lewis Carroll", "pub_date": 1865},
    {"book_id": 8, "title": "Animal Farm", "author": "George Orwell", "pub_date": 1945},
    {"book_id": 9, "title": "Anna Karenina", "author": "Leo Tolstoy", "pub_date": 1877},
    {"book_id": 10, "title": "Beloved", "author": "Toni Morrison", "pub_date": 1987},
    {"book_id": 11, "title": "Brave New World", "author": "Aldous Huxley", "pub_date": 1932},
    {"book_id": 12, "title": "Catch-22", "author": "Joseph Heller", "pub_date": 1961},
    {"book_id": 13, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "pub_date": 1866},
    {"book_id": 14, "title": "David Copperfield", "author": "Charles Dickens", "pub_date": 1850},
    {"book_id": 15, "title": "Don Quixote", "author": "Miguel de Cervantes", "pub_date": 1605},
    {"book_id": 16, "title": "Dracula", "author": "Bram Stoker", "pub_date": 1897},
    {"book_id": 17, "title": "Emma", "author": "Jane Austen", "pub_date": 1815},
    {"book_id": 18, "title": "Fahrenheit 451", "author": "Ray Bradbury", "pub_date": 1953},
    {"book_id": 19, "title": "Frankenstein", "author": "Mary Shelley", "pub_date": 1818},
    {"book_id": 20, "title": "Gone with the Wind", "author": "Margaret Mitchell", "pub_date": 1936},
    {"book_id": 21, "title": "Great Expectations", "author": "Charles Dickens", "pub_date": 1861},
    {"book_id": 22, "title": "Gulliver's Travels", "author": "Jonathan Swift", "pub_date": 1726},
    {"book_id": 23, "title": "Hamlet", "author": "William Shakespeare", "pub_date": 1603},
    {"book_id": 24, "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "pub_date": 1997},
    {"book_id": 25, "title": "Heart of Darkness", "author": "Joseph Conrad", "pub_date": 1899},
    {"book_id": 26, "title": "Jane Eyre", "author": "Charlotte Brontë", "pub_date": 1847},
    {"book_id": 27, "title": "Les Misérables", "author": "Victor Hugo", "pub_date": 1862},
    {"book_id": 28, "title": "Little Women", "author": "Louisa May Alcott", "pub_date": 1868},
    {"book_id": 29, "title": "Lolita", "author": "Vladimir Nabokov", "pub_date": 1955},
    {"book_id": 30, "title": "Lord of the Flies", "author": "William Golding", "pub_date": 1954},
    {"book_id": 31, "title": "Moby-Dick", "author": "Herman Melville", "pub_date": 1851},
    {"book_id": 32, "title": "Nineteen Eighty-Four", "author": "George Orwell", "pub_date": 1949},
    {"book_id": 33, "title": "Of Mice and Men", "author": "John Steinbeck", "pub_date": 1937},
    {"book_id": 34, "title": "Oliver Twist", "author": "Charles Dickens", "pub_date": 1838},
    {"book_id": 35, "title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez", "pub_date": 1967},
    {"book_id": 36, "title": "Pride and Prejudice", "author": "Jane Austen", "pub_date": 1813},
    {"book_id": 37, "title": "Rebecca", "author": "Daphne du Maurier", "pub_date": 1938},
    {"book_id": 38, "title": "Robinson Crusoe", "author": "Daniel Defoe", "pub_date": 1719},
    {"book_id": 39, "title": "Sense and Sensibility", "author": "Jane Austen", "pub_date": 1811},
    {"book_id": 40, "title": "Siddhartha", "author": "Hermann Hesse", "pub_date": 1922},
    {"book_id": 41, "title": "Slaughterhouse-Five", "author": "Kurt Vonnegut", "pub_date": 1969},
    {"book_id": 42, "title": "The Adventures of Huckleberry Finn", "author": "Mark Twain", "pub_date": 1884},
    {"book_id": 43, "title": "The Alchemist", "author": "Paulo Coelho", "pub_date": 1988},
    {"book_id": 44, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "pub_date": 1951},
    {"book_id": 45, "title": "The Chronicles of Narnia","author": "C.S. Lewis", "pub_date": 1950},
    {"book_id": 46, "title": "The Color Purple", "author": "Alice Walker", "pub_date": 1982},
    {"book_id": 47, "title": "The Count of Monte Cristo", "author": "Alexandre Dumas", "pub_date": 1844},
    {"book_id": 48, "title": "The Da Vinci Code", "author": "Dan Brown", "pub_date": 2003},
    {"book_id": 49, "title": "The Divine Comedy", "author": "Dante Alighieri", "pub_date": 1320},
    {"book_id": 50, "title": "The Fault in Our Stars", "author": "John Green", "pub_date": 2012},
    {"book_id": 51, "title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "pub_date": 1954},
    {"book_id": 52, "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "pub_date": 2005},
    {"book_id": 53, "title": "The Giving Tree", "author": "Shel Silverstein", "pub_date": 1964},
    {"book_id": 54, "title": "The Godfather", "author": "Mario Puzo", "pub_date": 1969},
    {"book_id": 55, "title": "The Golden Compass", "author": "Philip Pullman", "pub_date": 1995},
    {"book_id": 56, "title": "The Grapes of Wrath", "author": "John Steinbeck", "pub_date": 1939},
    {"book_id": 57, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "pub_date": 1925},
    {"book_id": 58, "title": "The Hobbit", "author": "J.R.R. Tolkien", "pub_date": 1937},
    {"book_id": 59, "title": "The Hunger Games", "author": "Suzanne Collins", "pub_date": 2008},
    {"book_id": 60, "title": "The Iliad", "author": "Homer", "pub_date": "8th century BC"},
    {"book_id": 61, "title": "The Interpretation of Dreams", "author": "Sigmund Freud", "pub_date": 1899},
    {"book_id": 62, "title": "The Jungle Book", "author": "Rudyard Kipling", "pub_date": 1894},
    {"book_id": 63, "title": "The Kite Runner", "author": "Khaled Hosseini", "pub_date": 2003},
    {"book_id": 64, "title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "pub_date": 1943},
    {"book_id": 65, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "pub_date": 1954},
    {"book_id": 66, "title": "The Lovely Bones", "author": "Alice Sebold", "pub_date": 2002},
    {"book_id": 67, "title": "The Metamorphosis", "author": "Franz Kafka", "pub_date": 1915},
    {"book_id": 68, "title": "The Odyssey", "author": "Homer", "pub_date": "8th century BC"},
    {"book_id": 69, "title": "The Old Man and the Sea", "author": "Ernest Hemingway", "pub_date": 1952},
    {"book_id": 70, "title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "pub_date": 1890},
    {"book_id": 71, "title": "The Pilgrim's Progress", "author": "John Bunyan", "pub_date": 1678},
    {"book_id": 72, "title": "The Prince", "author": "Niccolò Machiavelli", "pub_date": 1532},
    {"book_id": 73, "title": "The Scarlet Letter", "author": "Nathaniel Hawthorne", "pub_date": 1850},
    {"book_id": 74, "title": "The Secret Garden", "author": "Frances Hodgson Burnett", "pub_date": 1911},
    {"book_id": 75, "title": "The Shining", "author": "Stephen King", "pub_date": 1977},
    {"book_id": 76, "title": "The Silmarillion", "author": "J.R.R. Tolkien", "pub_date": 1977},
    {"book_id": 77, "title": "The Stranger", "author": "Albert Camus", "pub_date": 1942},
    {"book_id": 78, "title": "The Sun Also Rises", "author": "Ernest Hemingway", "pub_date": 1926},
    {"book_id": 79, "title": "The Three Musketeers", "author": "Alexandre Dumas", "pub_date": 1844},
    {"book_id": 80, "title": "The Time Machine", "author": "H.G. Wells", "pub_date": 1895},
    {"book_id": 81, "title": "The Trial", "author": "Franz Kafka", "pub_date": 1925},
    {"book_id": 82, "title": "The Twelfth Night", "author": "William Shakespeare", "pub_date": 1602},
    {"book_id": 83, "title": "The War of the Worlds", "author": "H.G. Wells", "pub_date": 1898},
    {"book_id": 84, "title": "The Wind in the Willows", "author": "Kenneth Grahame", "pub_date": 1908},
    {"book_id": 85, "title": "The Wonderful Wizard of Oz", "author": "L. Frank Baum", "pub_date": 1900},
    {"book_id": 86, "title": "The Yellow Wallpaper", "author": "Charlotte Perkins Gilman", "pub_date": 1892},
    {"book_id": 87, "title": "Things Fall Apart", "author": "Chinua Achebe", "pub_date": 1958},
    {"book_id": 88, "title": "To Kill a Mockingbird", "author": "Harper Lee", "pub_date": 1960},
    {"book_id": 89, "title": "Ulysses", "author": "James Joyce", "pub_date": 1922},
    {"book_id": 90, "title": "War and Peace", "author": "Leo Tolstoy", "pub_date": 1869},
    {"book_id": 91, "title": "Watership Down", "author": "Richard Adams", "pub_date": 1972},
    {"book_id": 92, "title": "Wuthering Heights", "author": "Emily Brontë", "pub_date": 1847},
    {"book_id": 93, "title": "2001: A Space Odyssey", "author": "Arthur C. Clarke", "pub_date": 1968},
    {"book_id": 94, "title": "A Christmas Carol", "author": "Charles Dickens", "pub_date": 1843},
    {"book_id": 95, "title": "A Clockwork Orange", "author": "Anthony Burgess", "pub_date": 1962},
    {"book_id": 96, "title": "A Confederacy of Dunces", "author": "John Kennedy Toole", "pub_date": 1980},
    {"book_id": 97, "title": "A Midsummer Night's Dream", "author": "William Shakespeare", "pub_date": 1595},
    {"book_id": 98, "title": "A Prayer for Owen Meany", "author": "John Irving", "pub_date": 1989},
    {"book_id": 99, "title": "A Room of One's Own", "author": "Virginia Woolf", "pub_date": 1929},
    {"book_id": 100, "title": "A Streetcar Named Desire", "author": "Tennessee Williams", "pub_date": 1947},
    {"book_id": 101, "title": "A Thousand Splendid Suns", "author": "Khaled Hosseini", "pub_date": 2007},
    {"book_id": 102, "title": "A Wrinkle in Time", "author": "Madeleine L'Engle", "pub_date": 1962},
    {"book_id": 103, "title": "All Quiet on the Western Front", "author": "Erich Maria Remarque", "pub_date": 1929},
    {"book_id": 104, "title": "American Gods", "author": "Neil Gaiman", "pub_date": 2001},
    {"book_id": 105, "title": "And Then There Were None", "author": "Agatha Christie", "pub_date": 1939},
    {"book_id": 106, "title": "Anne of Green Gables", "author": "L.M. Montgomery", "pub_date": 1908},
    {"book_id": 107, "title": "Atlas Shrugged", "author": "Ayn Rand", "pub_date": 1957},
    {"book_id": 108, "title": "Brideshead Revisited", "author": "Evelyn Waugh", "pub_date": 1945},
    {"book_id": 109, "title": "Charlotte's Web", "author": "E.B. White", "pub_date": 1952},
    {"book_id": 110, "title": "Cloud Atlas", "author": "David Mitchell", "pub_date": 2004},
    {"book_id": 111, "title": "Cold Mountain", "author": "Charles Frazier", "pub_date": 1997},
    {"book_id": 112, "title": "Dune", "author": "Frank Herbert", "pub_date": 1965},
    {"book_id": 113, "title": "East of Eden", "author": "John Steinbeck", "pub_date": 1952},
    {"book_id": 114, "title": "Fight Club", "author": "Chuck Palahniuk", "pub_date": 1996},
    {"book_id": 115, "title": "For Whom the Bell Tolls", "author": "Ernest Hemingway", "pub_date": 1940},
    {"book_id": 116, "title": "Foundation", "author": "Isaac Asimov", "pub_date": 1951},
    {"book_id": 117, "title": "Good Omens", "author": "Terry Pratchett and Neil Gaiman", "pub_date": 1990},
    {"book_id": 118, "title": "Gravity's Rainbow", "author": "Thomas Pynchon", "pub_date": 1973},
    {"book_id": 119, "title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "pub_date": 1999},
    {"book_id": 120, "title": "His Dark Materials", "author": "Philip Pullman", "pub_date": 1995},
    {"book_id": 121, "title": "I Know Why the Caged Bird Sings", "author": "Maya Angelou", "pub_date": 1969},
    {"book_id": 122, "title": "Infinite Jest", "author": "David Foster Wallace", "pub_date": 1996},
    {"book_id": 123, "title": "Invisible Man", "author": "Ralph Ellison", "pub_date": 1952},
    {"book_id": 124, "title": "It", "author": "Stephen King", "pub_date": 1986},
    {"book_id": 125, "title": "Jonathan Strange & Mr Norrell", "author": "Susanna Clarke", "pub_date": 2004},
    {"book_id": 126, "title": "Jurassic Park", "author": "Michael Crichton", "pub_date": 1990},
    {"book_id": 127, "title": "Leaves of Grass", "author": "Walt Whitman", "pub_date": 1855},
    {"book_id": 128, "title": "Life of Pi", "author": "Yann Martel", "pub_date": 2001},
    {"book_id": 129, "title": "Little House on the Prairie", "author": "Laura Ingalls Wilder", "pub_date": 1935},
    {"book_id": 130, "title": "Love in the Time of Cholera", "author": "Gabriel García Márquez", "pub_date": 1985},
    {"book_id": 131, "title": "Macbeth", "author": "William Shakespeare", "pub_date": 1623},
    {"book_id": 132, "title": "Middlemarch", "author": "George Eliot", "pub_date": 1871},
    {"book_id": 133, "title": "Midnight's Children", "author": "Salman Rushdie", "pub_date": 1981},
    {"book_id": 134, "title": "Mrs Dalloway", "author": "Virginia Woolf", "pub_date": 1925},
    {"book_id": 135, "title": "Native Son", "author": "Richard Wright", "pub_date": 1940},
    {"book_id": 136, "title": "Never Let Me Go", "author": "Kazuo Ishiguro", "pub_date": 2005},
    {"book_id": 137, "title": "On the Road", "author": "Jack Kerouac", "pub_date": 1957},
    {"book_id": 138, "title": "One Flew Over the Cuckoo's Nest", "author": "Ken Kesey", "pub_date": 1962},
    {"book_id": 139, "title": "Paradise Lost", "author": "John Milton", "pub_date": 1667},
    {"book_id": 140, "title": "Perfume: The Story of a Murderer", "author": "Patrick Süskind", "pub_date": 1985},
    {"book_id": 141, "title": "Peter Pan", "author": "J.M. Barrie", "pub_date": 1911},
    {"book_id": 142, "title": "Rebecca", "author": "Daphne du Maurier", "pub_date": 1938},
    {"book_id": 143, "title": "Sense and Sensibility", "author": "Jane Austen", "pub_date": 1811},
    {"book_id": 144, "title": "Slaughterhouse-Five", "author": "Kurt Vonnegut", "pub_date": 1969},
    {"book_id": 145, "title": "The Bell Jar", "author": "Sylvia Plath", "pub_date": 1963},
    {"book_id": 146, "title": "The Book Thief", "author": "Markus Zusak", "pub_date": 2005}
]


        for book_data in books_data:
            book = Book(book_data["book_id"], book_data["title"], book_data["author"], book_data["pub_date"])
            self.add_books(book)

        self.conn.commit()  


    def add_books(self, book):
        self.cursor.execute('''
            INSERT INTO books (book_id, title, author, pub_date)
            VALUES (?, ?, ?, ?)
        ''', (book.book_id, book.title, book.author, book.pub_date))
        self.conn.commit()

        print(f"Book added to the database: {book.title} by {book.author} ({book.pub_date})")
