from tkinter import *
from PIL import Image, ImageTk
import requests
import os
from io import BytesIO
from _book import Book
from _library import Library

class GalleryGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1242x600")
        self.root.title("Book Gallery")

        self.root_path = 'LibraryScanner/'
        self.library = Library(self.root_path+'library.csv')
        self.covers_folder = self.root_path+'covers/'
        self.get_covers()  # Checks for covers

        self.canvas_frame = Frame(self.root, width=750, padx=10, pady=10, bg="white")
        self.canvas_frame.pack(side=LEFT, fill=Y)

        #self.sort_frame = Frame(self.canvas_frame, height=30, padx=10, pady=10, bg="blue")
        #self.canvas_frame.pack(side=TOP, fill=X)
        # Sorting variables
        #self.sort_options = ["Title Ascending", "Title Descending", "Author Ascending", "Author Descending", "Date Ascending", "Date Descending"]
        #self.selected_sort = StringVar(value=self.sort_options[0])
        #self.sort_dropdown = OptionMenu(self.sort_frame, self.selected_sort, *self.sort_options, command=self.sort_books)
        #self.sort_dropdown.pack(side=RIGHT)

        self.canvas = Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)

        self.buttons = Frame(self.canvas_frame, bg="white", padx=10, pady=10)
        self.buttons.pack(side=BOTTOM, fill=X)

        self.add_button = Button(self.buttons, text="Add Book", command=self.add_book_button, padx=10)
        self.add_button.pack(pady=5, side=LEFT)

        # Sorting variables
        self.sort_options = ["Title Ascending", "Title Descending", "Author Ascending", "Author Descending", "Date Ascending", "Date Descending"]
        self.selected_sort = StringVar(value=self.sort_options[0])
        self.sort_dropdown = OptionMenu(self.buttons, self.selected_sort, *self.sort_options, command=self.sort_books)
        self.sort_dropdown.pack(side=LEFT)

        self.remove_button = Button(self.buttons, text="Remove Book", command=self.remove_book, padx=10)
        self.remove_button.pack(pady=5, side=RIGHT)
        
        self.selected_book = None  # To store the selected book

        self.sidebar = Frame(self.root, width=400, height=600, padx=10, pady=10, bg="white")
        self.sidebar.pack(side=RIGHT, after=self.canvas_frame, fill=BOTH)
        self.details_frame = Frame(self.sidebar, width=380, height=500, bg="white")
        self.details_frame.pack(side=LEFT, fill=BOTH)

        self.update_canvas()

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

    def sort_books(self, _):
        # Callback function for sorting
        sort_option = self.selected_sort.get()
        if sort_option == "Title Ascending":
            self.library.sort_books("title", reverse=False)
        elif sort_option == "Title Descending":
            self.library.sort_books("title", reverse=True)
        elif sort_option == "Author Ascending":
            self.library.sort_books("author", reverse=False)
        elif sort_option == "Author Descending":
            self.library.sort_books("author", reverse=True)
        elif sort_option == "Date Ascending":
            self.library.sort_books("published_date", reverse=False)
        elif sort_option == "Date Descending":
            self.library.sort_books("published_date", reverse=True)

        self.update_canvas()

    def add_book_button(self):
        new_window = Toplevel(self.root)
        isbn = StringVar()
        Label(new_window, text='Enter ISBN:').pack()
        Entry(new_window, textvariable=isbn).pack()
        Button(new_window, text='Ok', command=lambda: self.add_book_ok_button(isbn.get(), new_window)).pack()

    def add_book_ok_button(self, isbn, new_window):
        self.library.add_book(isbn)
        self.get_covers()  # Update covers
        self.update_canvas()  # Update canvas
        new_window.destroy()

    def remove_book(self):
        if self.selected_book:
            self.library.remove_book(self.selected_book.isbn)
            self.selected_book = None  # Clear the selection
            self.get_covers()  # Update covers
            self.update_canvas()  # Update canvas
            self.update_details_frame()  # Clear details frame

    def update_canvas(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

        row, col = 0, 0

        for isbn in self.library.books:
            book = self.library.books[isbn]

            # Load cover image
            cover_image_path = os.path.join(self.covers_folder, f"{isbn}.png")
            if os.path.exists(cover_image_path):
                img = ImageTk.PhotoImage(Image.open(cover_image_path).resize((100, 150), Image.LANCZOS))

                # Wrap text not more than 150 pixels wide
                title_label = Label(self.canvas, image=img, compound="top", padx=5, pady=5, font=("Helvetica", 10, "bold"), width=150, wraplength=150, bg="white")
                title_label.image = img

                # Bind the label to the book for selection
                title_label.bind("<Button-1>", lambda event, b=book: self.select_book(b))

                title_label.grid(row=row, column=col, padx=10, pady=15, sticky="n")

                col += 1
                if col == 5:
                    col = 0
                    row += 2  # Adjusting row for the author label

    def show_author_books(self, selected_author):
        author_books = [book for isbn, book in self.library.books.items() if book.author == selected_author]

        new_window = Toplevel(self.root)
        new_window.geometry("775x600")
        new_canvas = Canvas(new_window, bg="white")
        new_canvas.pack(fill=BOTH, expand=True)

        col, row = 0, 0
        for row, book in enumerate(author_books):
            cover_image_path = os.path.join(self.covers_folder, f"{book.isbn}.png")
            if os.path.exists(cover_image_path):
                img = ImageTk.PhotoImage(Image.open(cover_image_path).resize((100, 150), Image.LANCZOS))
                title_text = f"{book.title}"

                title_label = Label(new_canvas, image=img, text=title_text, compound="top", padx=5, pady=5, font=("Helvetica", 10), width=150, wraplength=150, bg="white")
                title_label.image = img

                title_label.bind("<Button-1>", lambda event, b=book: self.select_book(b))

                title_label.grid(row=row, padx=10, pady=5, sticky="n")

                col += 1
                if col == 5:
                    col = 0
                    row += 1

        new_window.mainloop()

    def select_book(self, book):
        if self.selected_book:
            self.selected_book = None
            self.update_canvas()  # Clear previous selection
        self.selected_book = book
        self.update_canvas()  # Highlight the selected book
        self.update_details_frame()  # Update details frame

    def update_details_frame(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        self.sidebar.config(width=400)
        self.details_frame.config(width=380, height=600)

        if self.selected_book:
            title_label = Label(self.details_frame, text=f"{self.selected_book.title}", font=("Helvetica", 14, "bold"), bg="white", wraplength=350)
            title_label.update_idletasks()  # Ensure frame dimensions are updated
            title_label.config(width=380)
            title_label.pack(fill=X,side=TOP)

            # Load larger cover image
            cover_image_path = os.path.join(self.covers_folder, f"{self.selected_book.isbn}.png")
            if os.path.exists(cover_image_path):
                larger_img = ImageTk.PhotoImage(Image.open(cover_image_path).resize((200, 300), Image.LANCZOS))
                larger_cover_label = Label(self.details_frame, image=larger_img, bg="white")
                larger_cover_label.image = larger_img
                larger_cover_label.pack(pady=10, fill=BOTH)

            author_label = Label(self.details_frame, text=f"{self.selected_book.author}", font=("Helvetica", 12), bg="white")
            author_label.pack()

            # Bind the author label to the book for showing author books
            author_label.bind("<Button-1>", lambda event, b=self.selected_book: self.show_author_books(b.author))

            ISBN_label = Label(self.details_frame, text=f"ISBN: {self.selected_book.isbn}", font=("Helvetica", 8), bg="white")
            ISBN_label.pack()

            pub_date_label = Label(self.details_frame, text=f"Publication Date: {self.selected_book.published_date}", font=("Helvetica", 8), bg="white")
            pub_date_label.pack()

if __name__ == "__main__":
    root = Tk()
    root.geometry("1242x600")
    app = GalleryGUI(root)
    root.mainloop()
