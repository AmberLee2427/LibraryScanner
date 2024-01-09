import requests

class Book:
    def __init__(self, isbn, title=None, author=None, published=None, cover=None):
        self.isbn = isbn.replace('-', '').replace(' ', '')
        self.title = title
        self.author = author
        self.published_date = published
        self.cover_image_url = cover

    def get_data(self):
        ''' Uses the 'isbn' class variable to query the Google Books catalogue

        DEPENDENCIES
        -------------
        requests

        NOTES
        ------
        Google Books API documentation:
        https://developers.google.com/books/docs/v1/using

        When trying decide which credentials to create for Google Cloud JSON API
        (https://console.cloud.google.com/apis/credentials?project=pythonlibraryscanner), 
        the recommendation is:
            This API doesn't require that you create credentials. 
            You're already good to go!
        '''
        api_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{self.isbn}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            # Extract relevant information from the API response
            if 'items' in data and data['items']:
                book_info = data['items'][0]['volumeInfo']
                self.title = book_info.get('title', 'N/A')
                self.author = ', '.join(book_info.get('authors', ['N/A']))
                self.published_date = book_info.get('publishedDate', 'N/A')

                # Choose the largest available cover image size
                # https://stackoverflow.com/questions/10721886/how-to-get-the-extra-large-cover-image-from-google-book-api
                image_links = book_info.get('imageLinks', {})
                sizes = ['extraLarge', 'large', 'medium', 'small', 'thumbnail', 'smallThumbnail']
                finding_biggest = True
                i = 0
                while finding_biggest:
                    size = sizes[i]
                    if size in image_links:
                        self.cover_image_url = image_links[size]
                        # The api will just give you the biggest image it has up to the number you set. 
                        # You can also set the height if you need to using e.g., '&fife=h900' 
                        # and both with e.g., '&fife=w800-h900'
                        self.cover_image_url = self.cover_image_url +'&fife=w600'
                        finding_biggest = False
                    i += 1
                    if i > len(sizes):  # cover image not found
                        self.cover_image_url = None
                        finding_biggest = False

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data from Google Books API: {e}")

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Published Date: {self.published_date}")

        #if self.cover_image_url is not None:
        #    display(Image(url=self.cover_image_url, width=200))
        print(f"Cover Image URL: {self.cover_image_url}")