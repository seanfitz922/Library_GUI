
class Book:
    def __init__(self, book_id, title, author, pub_date):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.pub_date = pub_date
        

    def display_details(self):
        print(f"Book ID: {self.book_id}")
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Publication Date: {self.pub_date}")
