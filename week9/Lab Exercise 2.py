# Lab Task 2: Library System with Composition

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_book_info(self):
        return f"'{self.title}' by {self.author}, ISBN: {self.isbn}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added: {book.display_book_info()}")

    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f"Removed: {book.display_book_info()}")
                return
        print(f"No book found with ISBN {isbn}.")

    def list_all_books(self):
        if not self.books:
            print("The library has no books")
        else:
            print("\nLibrary contains:")
            for i, book in enumerate(self.books, 1):
                print(f"  {i}. {book.display_book_info()}")

    def search_by_title(self, title):
        found = [book for book in self.books if title.lower() in book.title.lower()]
        if found:
            print(f"\nSearch results for '{title}' are:")
            for book in found:
                print(f"{book.display_book_info()}")
        else:
            print(f"No books found with title containing '{title}'")


#Test
if __name__ == "__main__":
    my_library = Library()

    book1 = Book("To Kill a Mockingbird", "Harper Lee", "978-1234567890")
    book2 = Book("Python Basics", "John Smith", "978-0987654321")
    book3 = Book("The Great Gatsby", "F. Scott Fitzgerald", "978-1122334455")

    my_library.add_book(book1)
    my_library.add_book(book2)
    my_library.add_book(book3)

    my_library.list_all_books()

    my_library.search_by_title("Python")
    my_library.search_by_title("Book")

    my_library.remove_book("978-0987654321")
    my_library.list_all_books()