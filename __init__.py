from _book import Book
from _gui import GalleryGUI

import tkinter as tk

# Example usage:
if __name__ == "__main__":

    # checking the Book class
    isbn_to_query = '9780141030012'
    book_instance = Book(isbn_to_query)
    book_instance.get_data()
    book_instance.display_info()

    root = tk.Tk()
    app = GalleryGUI(root)
    root.mainloop()