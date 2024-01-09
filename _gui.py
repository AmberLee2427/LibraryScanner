from tkinter import *
import requests
import os
from PIL import Image, ImageTk
from io import BytesIO

from _book import Book
from _library import Library

class GalleryGUI:
    def __init__(self, root):

        self.root = root
        self.root.title("Book Gallery")

        self.root_path = 'LibraryScanner/'
        self.library = Library(self.root_path+'library.csv')
        self.covers_folder = self.root_path+'covers/'
        self.get_covers() # checks for covers

        self.listbox = Listbox(root, height=35, width=50, selectmode=SINGLE)
        self.listbox.pack(pady=10)

        self.add_button = Button(root, text="Add Book", command=self.add_book_button)
        self.add_button.pack(side=LEFT, padx=10)
        
        self.remove_button = Button(root, text="Remove Book", command=self.remove_book)
        self.remove_button.pack(side=RIGHT, padx=10) 

        self.update_listbox()
        print('\n\n\n\n',self.library.books)

    def get_covers(self):
        for isbn in self.library.books:
            cover_path = os.path.join(self.covers_folder, f"{isbn}.png")
            if not os.path.exists(cover_path):
                self.get_cover(isbn, cover_path)       

    def get_cover(self, isbn, cover_path):
        book = self.library.books[isbn]
        cover_image_url = book.cover_image_url
        if cover_image_url:
            response = requests.get(cover_image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image.save(cover_path)

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
        self.get_covers()
        for isbn in self.library.books:
            book = self.library.books[isbn]
            self.listbox.insert(END, f"{book.title} ({book.isbn})")