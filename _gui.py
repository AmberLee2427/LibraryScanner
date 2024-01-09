from tkinter import *
import requests

from _book import Book

class GalleryGUI:
    def __init__(self, root):

        self.root = root
        self.root.title("Book Gallery")

        self.books = []  # List to store Book objects

        self.listbox = Listbox(root, height=10, selectmode=SINGLE)
        self.listbox.pack(pady=10)

        self.add_button = Button(root, text="Add Book", command=self.add_book_button)
        self.add_button.pack(side=LEFT, padx=10)
        
        self.remove_button = Button(root, text="Remove Book", command=self.remove_book)
        self.remove_button.pack(side=RIGHT, padx=10)

    def add_book(self,isbn):
        book_instance = Book(isbn)
        book_instance.get_data()
        self.books.append(book_instance)
        self.update_listbox()

    def add_book_button(self):
        isbn=StringVar()
        Label(self.root, text='Enter ISBN:').pack()
        Entry(self.root, textvariable=isbn).pack()
        Button(self.root, text='Ok', command=lambda:self.add_book(isbn.get)).pack()
 
    def remove_book(self):
        selected_index = self.listbox.curselection()
        del self.books[selected_index[0]]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, END)
        for book in self.books:
            self.listbox.insert(END, f"{book.title} ({book.isbn})")