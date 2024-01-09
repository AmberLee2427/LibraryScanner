import csv
import os

from _book import Book

class Library:
    def __init__(self, library_file=None):
        
        if library_file is None:
            library_file = 'library.csv'
        self.library_file = library_file

        self.books = {}  # empty shelves
        self.header = ['isbn', 'title', 'author', 'published', 'cover']  # the basic header

        if not os.path.exists(library_file):
            # Create an empty CSV file
            with open(library_file, 'w', newline=''):
                pass
        self.load_books(library_file)

        self.sort_books('title')

    def load_books(self,library_file=None):
        ''' can be used to merge multiple library_files'''
        if library_file is None:
             library_file = self.library_file

        with open(library_file, 'r', newline='') as file:
            reader = csv.DictReader(file) 
            for row in reader:
                # need to reslove duplicates
                self.books[row['isbn']] = Book(row['isbn'], title=row['title'], author=row['author']\
                                               , published=row['published'], cover=row['cover'])
            
            #new_header = row.keys()
            # will need to resolve header merging when extra columns are optionally added
            
            # will need to tack on extra column options when added.

    def save_library(self, save_as=False):
        ''' overwrites the library csv file (self.library_file; default='Library.csv')

        DEPENDENCIES
        -------------
        csv

        OPTIONAL INPUTS
        ----------------
        save_as:        type: boolean/string
                        contains: *file_path* of type string to save the library csv to;
                                    False (defaul) saves to './library.csv'
        '''

        if save_as:  # True for strings
             file_path = save_as
        else:
             file_path = self.library_file
        with open(file_path, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=self.header)
                    writer.writeheader()
                    for isbn in self.books:
                        book = self.books[isbn]
                        #print(self.book_to_dict(book))
                        writer.writerow(self.book_to_dict(book))

    def book_to_dict(self, book):
        dic_book = {'isbn': book.isbn, 'title': book.title, 'author':book.author\
                    , 'published':book.published_date, 'cover':book.cover_image_url}
        # will need to add extra columns later
        return dic_book
    
    def sort_books(self, key, reverse=False):
        '''Sort the books based on the specified key and order.

        INPUTS
        -------
        key:        type: string
                    contains: the key to sort the books by 
                                (e.g., 'title', 'author', 'published_date').

        OPTIONAL INPUTS
        ----------------
        reverse:    type: boolean
                    contains: True, if sorting in descending order; 
                                False (default), if sorting in ascending order.
        '''
        if key not in self.header:
            raise ValueError(f"Invalid key '{key}'. Supported keys: {', '.join(self.header)}")

        # Sort books based on the specified key
        self.books = dict(sorted(self.books.items(), key=lambda x: getattr(x[1], key), reverse=reverse))

    def add_book(self, isbn, save=True):
        if not (isbn in self.books.keys()):
            book_object = Book(isbn)
            book_object.get_data()

            self.books[isbn] = book_object 
        
            if save:
                self.save_library()
        #else:  # add a copies column

    def add_books(self,isbn_book_list):
        ''' adds all the books in the provided list to the library file. 
         Saves once at the end of the process

         INPUTS
         -------
         isbn_book_list:    type: list
                            subtype: string (10 or 13 digit real, whole numbers)
                            contains: a list of ISBN numbers as strings
        '''

        for book_isbn in isbn_book_list:
            self.add_book(book_isbn, save=False)
        self.save_library()

    def remove_book(self,isbn):
        '''Remove a book from the library.

        INPUTS
        -------
        isbn:       type: string
                    contains: the ISBN of the book to be removed.
        '''
        if isbn in self.books:
            del self.books[isbn]
            self.save_library()
        else:
            print(f"Book with ISBN {isbn} not found in the library.")