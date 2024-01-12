import csv
import os
import requests
from collections import namedtuple
import pickle

from _book import Book

class Library:
    def __init__(self, library_file=None):
        
        self.csv = 'library.csv'
        if library_file is None:
            library_file = self.csv
        self.library_file = library_file
        self.pickle = 'library.pickle'

        self.books = []  # empty shelves
        self.header = ['isbn', 'title', 'author', 'published_date', 'description', \
                       'page_count', 'average_rating', 'ratings_count', 'categories', \
                        'maturity_rating', 'cover']
        self.book_keys = []
        
        self.user_specific = []
        self.empty_field = []
        self.user_fields = []  # e.g. user rating, user review, loaned to ...

        self.database_type = 'pickle'  # or 'csv'

        if os.path.exists(library_file):
            self.load_books(library_file)
        else:
            # Create an empty CSV file
            with open(library_file, 'w', newline=''):
                pass

        self.sort_books('title')

    def load_books(self,library_file=None):
        ''' can be used to merge multiple library_files'''

        if '.csv' in library_file:
            try:
                with open(library_file, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # need to reslove duplicates
                        if row['isbn'] in self.book_keys:
                            pass
                        else:
                            self.books.append(row)
                            self.book_keys.append(row['isbn'])
            except Exception as e:
                print("Error during loading of csv:", e)                

        else:
            try:
                with open(library_file, "rb") as f:
                    loaded_data = pickle.load(f)
                    self.books.extend(loaded_data.books)
                    self.book_keys.extend([book['isbn'] for book in loaded_data.books])
            except Exception as e:
                print("Error during unpickling object (Possibly unsupported):", e) 

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
        elif self.database_type == 'csv':
            file_path = self.csv
        elif self.database_type == 'pickle':
            file_path = self.pickle

        if 'csv' in file_path:  
            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.header)
                writer.writeheader()
                for book in self.books:
                    writer.writerow(book)

        # save pickle instead
        else:
            try:
                with open(file_path, "wb") as f:
                    pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print("Error during pickling object (Possibly unsupported):", e)
    
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
        self.books = sorted(self.books, key=lambda x: x.get(key, ''), reverse=reverse)

    def add_field(self, field, empty=None):
        '''
        INPUTS
        -------
        field:      type: string
                    contains: a name for the new field

        OPTIONAL INPUTS
        ----------------
        empty:      type: any (default is None)
                    contains: an empty item of the data type intended for this field

        '''
        self.user_fields = field
        self.empty_field = empty

        # add field to existing books
        #load library
        #save library

    def remove_field(self, field):
        ''' '''
        pass

    def rename_field(self, old_field, new_field):
        ''' '''
        pass

    def add_book(self, isbn, save=True):
        ''' adds a book to the class dictionary self.books, by fetching meta data 
        using the class function get_book_data, and creating a blank user_data dict.
        
        INPUTS
        -------
        isbn        type: string

        OPTIONAL INPUTS
        ----------------
        save:       type: boolean
        '''
        if not (isbn in self.book_keys): # if not already in the self.books list
            self.book_keys.append(isbn)

            # API metadata
            api_data = self.get_book_data(isbn)  # uses the Google books API
            if api_data is not None:
                # add 
                self.books.append(api_data)

            # empty user data
            user_data = {}
            for i, field in enumerate(self.user_fields):
                user_data[field] = self.empty_field[i]
            self.user_specific.append(user_data)
            
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
            self.add_book(book_isbn, save=True)

    def get_book_data(self, isbn):
        ''' Uses the 'isbn' variable to query the Google Books catalogue
        
        INPUTS
        -------
        isbn:       type: string (10 or 13 digit real, whole numbers)
                    contains: book ISBN as a string

        DEPENDENCIES
        -------------
        requests
        collection.namedtuple - or not

        NOTES
        ------
        Google Books API documentation:
        https://developers.google.com/books/docs/v1/using

        When trying decide which credentials to create for Google Cloud JSON API
        (https://console.cloud.google.com/apis/credentials?project=pythonlibraryscanner), 
        the recommendation is:
            This API doesn't require that you create credentials. 
            You're already good to go!

        The JSON includes a bunch of shit. It gets converted into a dict by requests.
        The dictionary contains:
            * 'kind',               (str: I'm guessing this API isn't just used for books)
            * 'totalItems',         (int: I'm guessing this is only ever 1 for books)
            * 'items'.              (list: this is a list of length totalItems)
        Each item in the list is a dict containing:
            * 'kind',               (str: same as above)
            * 'id',                 (str)
            * 'etag',               (str)
            * 'selfLink',           (str: url)
            * 'volumeInfo',         (dic)
            * 'saleInfo',           (price stuff)
            * 'accessInfo',         (info about api call)
            * 'searchInfo'.         (google search stuff)
        The important stuff seems to be in dict['items'][0]['volumeInfo'], which contains:

        I don't know why there would ever be more than one item.
        volume_info contains:
            * 'title',              (str)
            * 'subtitle',           (str: nonsense)
            * 'authors',            (list: of strings with auhtor names)
            * 'publisher',          (str)
            * 'publishedDate',      (str: e.g. '2016', '2016-03-21')
            * 'description',        (str: contains blurb)
            * 'industryIdentifiers',(list: containing dictionaries with entries for type and identifier, e.g. ISBN-10)
            * 'readingModes',       (dict: ?)
            * 'pageCount',          (int)
            * 'printType',          (str: 'BOOK')
            * 'categories',         (list of strings e.g. 'Fiction')
            * 'averageRating',      (float)
            * 'ratingsCount',       (int)
            * 'maturityRating',     (str: e.g. 'NOT_MATURE')
            * 'allowAnonLogging',   (bool)
            * 'contentVersion',     (str)
            * 'panelizationSummary',(dict: ?)
            * 'imageLinks',         (dict: contains str of URLs to cover images)
                                    (keys: e.g 'smallTumbnail', 'thumbnail')
            * 'language',           (str: e.g. 'en')
            * 'previewLink',        (str: URLs)
            * 'infoLink',           (str: URLs)
            * 'canonicalVolumeLink'.(str: URLs) 
        '''
        api_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant information from the API response
            book_info = data['items'][0]['volumeInfo']
            title = book_info.get('title', 'N/A')
            author = ', '.join(book_info.get('authors', ['N/A']))
            published_date = book_info.get('publishedDate', 'N/A')
            description = book_info.get('description', 'N/A')
            page_count = book_info.get('pageCount', 'N/A')
            average_rating = book_info.get('averageRating', 'N/A')
            ratings_count = book_info.get('ratingsCount', 'N/A')
            categories = book_info.get('categories', 'N/A')
            maturity_rating = book_info.get('maturityRating', 'N/A')

            # Choose the largest available cover image size
            # https://stackoverflow.com/questions/10721886/how-to-get-the-extra-large-cover-image-from-google-book-api
            image_links = book_info.get('imageLinks', {})
            sizes = ['extraLarge', 'large', 'medium', 'small', 'thumbnail', 'smallThumbnail']
            finding_biggest = True
            i = 0
            while finding_biggest:
                size = sizes[i]
                if size in image_links:
                    cover_image_url = image_links[size]
                    # The api will just give you the biggest image it has up to the number you set. 
                    # You can also set the height if you need to using e.g., '&fife=h900' 
                    # and both with e.g., '&fife=w800-h900'
                    cover_image_url = cover_image_url +'&fife=w600'
                    finding_biggest = False
                i += 1
                if i > len(sizes):  # cover image not found
                    cover_image_url = None
                    finding_biggest = False

            #Book = namedtuple("Book", self.header)
            #book = Book(isbn, title, author, published_date, description, page_count,\
            #        average_rating, ratings_count, categories, maturity_rating)
                    
            # book as a dictionary
            meta_data_list = [isbn, title, author, published_date, description, \
                              page_count, average_rating, ratings_count, categories, \
                                maturity_rating, cover_image_url]
            book = {}
            for i, key in enumerate(self.header):
                book[key] = meta_data_list[i]

            return book

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data from Google Books API: {e}")

            return None

    def remove_book(self,isbn):
        '''Remove a book from the library.

        INPUTS
        -------
        isbn:       type: string
                    contains: the ISBN of the book to be removed.
        '''
        if isbn in self.book_keys:
            # remove entry for self.books
            for i, book in enumerate(self.books):
                if book['isbn'] == isbn:
                    del self.books[i]

            # remove entry from keys
            del self.book_keys[self.book_keys.index(isbn)]

            # update programe data
            self.save_library()
        else:
            print(f"Book with ISBN {isbn} not found in the library.")