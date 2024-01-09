from tkinter import *
import requests

from _book import Book
from _library import Library

class GalleryGUI:
    def __init__(self, root):

        self.root = root
        self.root.title("Book Gallery")

        self.library = Library('LibraryScanner/library.csv')

        self.listbox = Listbox(root, height=35, width=50, selectmode=SINGLE)
        self.listbox.pack(pady=10)

        self.add_button = Button(root, text="Add Book", command=self.add_book_button)
        self.add_button.pack(side=LEFT, padx=10)
        
        self.remove_button = Button(root, text="Remove Book", command=self.remove_book)
        self.remove_button.pack(side=RIGHT, padx=10) 

        self.update_listbox()
        print('\n\n\n\n',self.library.books) 

    def add_book_button(self):
        new_window = Toplevel(self.root)
        isbn=StringVar()
        Label(new_window, text='Enter ISBN:').pack()
        Entry(new_window, textvariable=isbn).pack()
        Button(new_window, text='Ok', command=lambda: self.add_book_ok_button(isbn.get(), new_window)).pack()

    def add_book_ok_button(self, isbn, new_window):
        self.library.add_book(isbn)
        self.update_listbox()
        new_window.destroy()
        
    def remove_book(self):
        selected_index = self.listbox.curselection()
        del self.books[selected_index[0]]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, END)
        for isbn in self.library.books:
            book = self.library.books[isbn]
            self.listbox.insert(END, f"{book.title} ({book.isbn})")