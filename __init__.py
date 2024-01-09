from _book import Book
from _gui import GalleryGUI
from _library import Library

import tkinter as tk

# Example usage:
if __name__ == "__main__":

    # checking the Book class
    #isbn_to_query = '9780141030012'
    #book_instance = Book(isbn_to_query)
    #book_instance.get_data()
    #book_instance.display_info()

    # testing the Library class
    #new_library = Library('LibraryScanner/library.csv')
    #isbns_to_query = ['978-1-60309-514-3', '978-1-60309-385-9', '978-1-60309-524-2']
    #new_library.add_books(isbns_to_query)

    #testing the GUI
    root = tk.Tk()
    root.geometry("1242x600")
    app = GalleryGUI(root)
    root.mainloop()