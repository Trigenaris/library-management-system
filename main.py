import os
import sqlite3
import csv
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


class Book:
    """
    Class representing a book.
    """
    def __init__(self, title, author, publisher, published_year, rating, isbn):
        """
        Initialize a Book object.
        :param title (str): The title of the book.
        :param author (str): The author of the book.
        :param publisher (str): The publisher of the book.
        :param published_year (str): The year the book was published.
        :param rating (str): The rating of the book.
        :param isbn (str): The ISBN of the book.
        """
        self.title = title
        self.author = author
        self.publisher = publisher
        self.published_year = published_year
        self.rating = rating
        self.isbn = isbn


class Member:
    """
    Class representing a library member.
    """
    def __init__(self, first_name, last_name, email, gender, state, member_no):
        """
        Initialize a Member object.
        :param first_name (str): The first name of the member.
        :param last_name (str): The last name of the member.
        :param email (str): The email address of the member.
        :param gender (str): The gender of the member.
        :param state (str): The state of the member.
        :param member_no (str): The unique member number of the member.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.state = state
        self.member_no = member_no


class Library:
    """
    Class representing a library and its operations.
    """
    def __init__(self):
        """
        Initialize the Library object and connect to the database.
        """
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """
        Create necessary tables in the database if they do not exist.
        :return: None
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BOOKS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TITLE VARCHAR(300),
                AUTHOR VARCHAR(100),
                PUBLISHER VARCHAR(200),
                PUBLISHED_YEAR SMALLINT,
                RATING FLOAT,
                ISBN VARCHAR(11)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS MEMBERS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                FIRST_NAME VARCHAR(100),
                LAST_NAME VARCHAR(100),
                EMAIL VARCHAR(200),
                GENDER VARCHAR(15),
                STATE VARCHAR(20),
                MEMBER_NO VARCHAR(11)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS LEND_BOOKS (
                BOOK_ID INTEGER,
                MEMBER_ID INTEGER,
                FOREIGN KEY (BOOK_ID) REFERENCES BOOKS(ID),
                FOREIGN KEY (MEMBER_ID) REFERENCES MEMBERS(ID),
                PRIMARY KEY (BOOK_ID, MEMBER_ID)
            )
        ''')
        self.conn.commit()

    def _book_validation(self, book):
        """
        Check if a book with the same ISBN already exists in the database.
        :param book (Book): The book object to validate.
        :return: result: The result of the validation query.
        """
        self.cursor.execute('SELECT ID FROM BOOKS WHERE ISBN = ?', (book.isbn,))
        result = self.cursor.fetchone()
        return result if result else None

    def add_book(self, book):
        """
        Add a book to the library database.
        :param book (Book): The book object to add to the database.
        :return: None
        """
        if not self._book_validation(book):
            self.cursor.execute('''INSERT INTO books (TITLE, AUTHOR, PUBLISHER, PUBLISHED_YEAR, RATING, ISBN)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                                (book.title, book.author, book.publisher,
                                 book.published_year, book.rating, book.isbn))
            self.conn.commit()
        else:
            print("Invalid book!")

    def _get_book_id(self, title):
        """
        Get the ID of a book by its title from the database.
        :param title (str): The title of the book.
        :return: (int) The ID of the book.
        """
        self.cursor.execute('SELECT ID FROM BOOKS WHERE TITLE = ?', (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def remove_book(self, title):
        """
        Remove a book from the library database by its title.
        :param title (str): The title of the book to remove.
        :return: None
        """
        book_id = self._get_book_id(title)
        if book_id:
            self.cursor.execute('DELETE FROM BOOKS WHERE ID=?', (book_id,))
            self.conn.commit()
            print("book deleted!")
            return True
        else:
            print("no book!")
            return False

    def _member_validation(self, member):
        """
        Check if a member with the same member number already exists in the database.
        :param member (Member): The member object to validate.
        :return: result: The result of the validation query.
        """
        self.cursor.execute('SELECT ID FROM MEMBERS WHERE MEMBER_NO = ?', (member.member_no,))
        result = self.cursor.fetchone()
        return result if result else None

    def register_member(self, member):
        """
        Register a member in the library database.
        :param member (Member): The member object to register.
        :return: None
        """
        if not self._member_validation(member):
            self.cursor.execute('''INSERT INTO members (FIRST_NAME, LAST_NAME, EMAIL, GENDER, STATE, MEMBER_NO)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                                (member.first_name, member.last_name, member.email,
                                 member.gender, member.state, member.member_no))
            self.conn.commit()
        else:
            print("Invalid member!")

    def _get_member_id(self, member_no):
        """
        Get the ID of a member by their member number from the database.
        :param member_no (str): The member number of the member.
        :return: (int) The ID of the member.
        """
        self.cursor.execute("SELECT ID FROM MEMBERS WHERE MEMBER_NO = ?", (member_no,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def remove_member(self, member_no):
        """
        Remove a member from the library database by their member number.
        :param member_no (str): The member number of the member to remove.
        :return: None
        """
        member_id = self._get_member_id(member_no)
        if member_id:
            self.cursor.execute("DELETE FROM MEMBERS WHERE ID = ?", (member_id,))
            self.conn.commit()
            print(f"The member with the {member_no} member no, has been deleted from the system.")
            return True
        else:
            print("This member cannot be found.")
            return False

    def add_books_from_csv(self, filename):
        """
        Add multiple books to the library database from a CSV file.
        :param filename (str): The path to the CSV file containing book information.
        :return: None
        """
        with open(file=filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                book = Book(
                    title=row['title'],
                    author=row['author'],
                    publisher=row['publisher'],
                    published_year=row['published_year'],
                    rating=row['rating'],
                    isbn=row['ISBN']
                )
                self.add_book(book)

    def register_members_from_csv(self, filename):
        """
        Register multiple members in the library database from a CSV file.
        :param filename (str): The path to the CSV file containing member information.
        :return: None
        """
        with open(file=filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                member = Member(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    gender=row['gender'],
                    state=row['state'],
                    member_no=row['member_no']
                )
                self.register_member(member)

    def select_books(self):
        """
        Retrieve all books from the database.
        :return: (list) A list of dicts containing book information.
        """
        self.cursor.execute("SELECT * FROM BOOKS")
        books = self.cursor.fetchall()
        return books

    def select_members(self):
        """
        Retrieve all members from the database.
        :return: (list) A list of dicts containing member information.
        """
        self.cursor.execute("SELECT * FROM MEMBERS")
        members = self.cursor.fetchall()
        return members

    def select_one_book(self, title):
        """
        Retrieve the selected book from the database.
        :param book_title (str): The title of the book to be borrowed.
        :return: (obj) Returns a book object.
        """
        book_id = self._get_book_id(title)
        if book_id:
            book = self.cursor.execute('SELECT TITLE FROM BOOKS WHERE ID=?', (book_id,)).fetchone()
            return book if book else None

    def select_one_member(self, member_no):
        """
        Retrieve the selected member from the database.
        :param member_no (int): The title of the member to be borrowed.
        :return: (obj) Returns a member object.
        """
        member_id = self._get_member_id(member_no)
        if member_id:
            member = self.cursor.execute('SELECT * FROM MEMBERS WHERE ID=?', (member_id,)).fetchone()
            return member if member else None

    def lent_books(self):
        """
        Retrieve all lent books along with member information from the database.
        :return: (list) A list of dictionaries containing lent book information along with member details.
        """
        self.cursor.execute('''
        SELECT 
            BO.TITLE AS BOOK_TITLE,
            ME.FIRST_NAME AS MEMBER_FIRST_NAME,
            ME.LAST_NAME AS MEMBER_LAST_NAME
        FROM BOOKS AS BO
        JOIN LEND_BOOKS ON BOOK_ID = BO.ID
        JOIN MEMBERS AS ME ON MEMBER_ID = ME.ID
        ''')
        lent_books = self.cursor.fetchall()
        return lent_books

    def lend_book(self, title, member_no):
        """
        Allow a member to borrow a book from the library.
        :param book_title (str): The title of the book to be borrowed.
        :param member_no (str): The member number of the member borrowing the book.
        :return: None
        """
        book_id = self._get_book_id(title)
        member_id = self._get_member_id(member_no)
        if book_id and member_id:
            self.cursor.execute("SELECT * FROM LEND_BOOKS WHERE BOOK_ID = ?", (book_id,))
            current_lending = self.cursor.fetchone()
            if current_lending:
                print(f"The book named {title} is already lent.")
                return False
            else:
                self.cursor.execute("INSERT INTO LEND_BOOKS (BOOK_ID, MEMBER_ID) VALUES (?,?)",
                                    (book_id, member_id))
                self.conn.commit()
                print(f"The book named {title} is lent by the member with {member_no} member no.")
                return True
        else:
            print("Unknown book name or member no.")
            return False

    def return_book(self, title):
        """
        Allow a member to return a borrowed book to the library.
        :param book_title (str): The title of the book to be returned.
        :return: None
        """
        book_id = self._get_book_id(title)
        if book_id:
            self.cursor.execute("SELECT * FROM LEND_BOOKS WHERE BOOK_ID=?", (book_id,))
            current_lending = self.cursor.fetchone()
            if current_lending:
                self.cursor.execute("DELETE FROM LEND_BOOKS WHERE BOOK_ID=?", (book_id,))
                self.conn.commit()
                print(f"{title} has returned to the library system.")
                return True
            else:
                print(f"{title} is already in the library.")
                return False
        else:
            print("Unknown book name.")
            return False


class LibraryGUI:
    def __init__(self, root):
        """
        Initialize the Library Management System GUI.
        :param root: The main window of the app.
        """
        self.root = root
        self.root.title("Library Management System")
        self.root.config(padx=20, pady=20, bg="white")
        self.display_width = root.winfo_screenwidth()
        self.display_height = root.winfo_screenheight()
        self.left = int(self.display_width / 2 - (660 / 2))
        self.top = int(self.display_height / 2 - (500 / 2))
        self.root.geometry(f"660x500+{self.left}+{self.top}")
        self.root.resizable(False, False)

        self.title_label = ttk.Label(root, text="Daisy Library Management",
                                     font=("Helvetica", 16, "bold"), background="white")
        self.title_label.grid(row=0, column=1, pady=10)

        self.canvas = tk.Canvas(root, width=200, height=200, highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=3)
        self.logo_image = tk.PhotoImage(file="daisy_logo.png")
        self.canvas.create_image(100, 100, image=self.logo_image)

        self.show_books_button = ttk.Button(root, text="Show Books", command=self.show_books)
        self.show_books_button.grid(row=2, column=0)
        self.show_members_button = ttk.Button(root, text="Show Members", command=self.show_members)
        self.show_members_button.grid(row=2, column=1)
        self.show_lent_books_button = ttk.Button(root, text="Show Lent Books", command=self.show_lent_books)
        self.show_lent_books_button.grid(row=2, column=2)

        self.paned_window_visibility = False
        self.paned_window_button = ttk.Button(root, text="More Options", command=self.toggle_paned_window)
        self.paned_window_button.grid(row=3, column=0, rowspan=2, padx=10, pady=10)
        self.paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="white")

        self.quit_button = ttk.Button(root, text="Exit", command=exit)
        self.quit_button.grid(row=3, column=2)

        self.add_book_button = ttk.Button(self.paned_window, text="Add Book", command=self.adding_book)
        self.add_book_button.pack()
        self.remove_book_button = ttk.Button(self.paned_window, text="Remove Book", command=self.removing_book)
        self.remove_book_button.pack()
        self.register_member_button = ttk.Button(self.paned_window, text="Register Member", command=self.adding_member)
        self.register_member_button.pack()
        self.remove_member_button = ttk.Button(self.paned_window, text="Remove Member", command=self.removing_member)
        self.remove_member_button.pack()
        self.lend_book = ttk.Button(self.paned_window, text="Lend Book", command=self.lend_book_process)
        self.lend_book.pack()
        self.return_book = ttk.Button(self.paned_window, text="Return Book", command=self.return_book_process)
        self.return_book.pack()
        self.add_csv_books_button = ttk.Button(self.paned_window,
                                               text="Add Multiple Books\n(CSV only)",
                                               command=self.add_books_from_csv)
        self.add_csv_books_button.pack()
        self.add_csv_members_button = ttk.Button(self.paned_window,
                                                 text="Add Multiple Members\n(CSV only",
                                                 command=self.add_members_from_csv)
        self.add_csv_members_button.pack()
        self.url_label = tk.Label(self.paned_window, text="About us", fg="blue", bg="white", cursor="hand2")
        self.url_label.pack()
        self.url_label.bind("<Button-1>", self.open_html)

        self.library = Library()

    def show_books(self):
        """
        Display the list of books in a new window.
        :return: None
        """
        books_window = tk.Toplevel(self.root)
        books_window.title("Books")
        books = self.library.select_books()
        if not books:
            messagebox.showwarning(title="Error!", message="There are no books in the system!")
            books_window.destroy()
        else:
            tree_frame = ttk.Frame(books_window)
            tree_frame.pack(fill=tk.BOTH, expand=True)

            book_tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Author", "Publisher",
                                                          "Published Year", "Rating", "ISBN"), show="headings")
            book_tree.heading("ID", text="ID")
            book_tree.heading("Title", text="Title")
            book_tree.heading("Author", text="Author")
            book_tree.heading("Publisher", text="Publisher")
            book_tree.heading("Published Year", text="Published Year")
            book_tree.heading("Rating", text="Rating")
            book_tree.heading("ISBN", text="ISBN")
            for book in books:
                book_tree.insert("", "end", values=book)

            book_tree.config(height=30)
            tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=book_tree.yview)
            book_tree.configure(yscrollcommand=tree_scroll.set)
            book_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def show_members(self):
        """
        Display the list of members in a new window.
        :return: None
        """
        members_window = tk.Toplevel(self.root)
        members_window.title("Members")
        members = self.library.select_members()
        if not members:
            messagebox.showwarning(title="Error!", message="There are no registered members in the system!")
            members_window.destroy()
        else:
            tree_frame = ttk.Frame(members_window)
            tree_frame.pack(fill=tk.BOTH, expand=True)

            member_tree = ttk.Treeview(tree_frame, columns=("ID", "First Name", "Last Name", "Email",
                                                            "Gender", "State", "Member No"), show="headings")
            member_tree.heading("ID", text="ID")
            member_tree.heading("First Name", text="First Name")
            member_tree.heading("Last Name", text="Last Name")
            member_tree.heading("Email", text="Email")
            member_tree.heading("Gender", text="Gender")
            member_tree.heading("State", text="State")
            member_tree.heading("Member No", text="Member No")
            for member in members:
                member_tree.insert("", "end", values=member)

            member_tree.config(height=30)
            tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=member_tree.yview)
            member_tree.configure(yscrollcommand=tree_scroll.set)
            member_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def show_lent_books(self):
        """
        Display the list of lent books in a new window.
        :return: None
        """
        lent_books_window = tk.Toplevel(self.root)
        lent_books_window.title("Lent Books")
        lent_books = self.library.lent_books()

        if not lent_books:
            messagebox.showinfo("No Lent Books", "There are no lent books at the moment.")
            lent_books_window.destroy()
        else:
            lent_books_tree = ttk.Treeview(lent_books_window,
                                           columns=("Book Title", "Member First Name", "Member Last Name"),
                                           show="headings")
            lent_books_tree.heading("Book Title", text="Book Title")
            lent_books_tree.heading("Member First Name", text="Member First Name")
            lent_books_tree.heading("Member Last Name", text="Member Last Name")

            for book in lent_books:
                lent_books_tree.insert("", "end", values=book)

            lent_books_tree.pack()

    def toggle_paned_window(self):
        """
        Toggle the visibility of the additional option pane.
        :return: None
        """
        if self.paned_window_visibility:
            self.paned_window.grid_forget()
            self.paned_window_visibility = False
        else:
            self.paned_window.grid(row=1, column=3, rowspan=2, sticky="nsew")
            self.paned_window_visibility = True

    def adding_book(self):
        """
        Open a window to add a new book to the library.
        :return: None
        """
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("New Book Information")
        add_book_window.geometry("500x200")
        add_book_window.resizable(False, False)

        info_label = tk.Label(add_book_window, text="Please enter the information of the book: ")
        info_label.grid(row=0, column=0, padx=5, pady=5)

        title_label = tk.Label(add_book_window, text="Title: ")
        title_label.grid(row=1, column=0)
        title_entry = ttk.Entry(add_book_window, width=30)
        title_entry.grid(row=1, column=1)

        author_label = tk.Label(add_book_window, text="Author: ")
        author_label.grid(row=2, column=0)
        author_entry = ttk.Entry(add_book_window, width=30)
        author_entry.grid(row=2, column=1)

        publisher_label = tk.Label(add_book_window, text="Publisher: ")
        publisher_label.grid(row=3, column=0)
        publisher_entry = ttk.Entry(add_book_window, width=30)
        publisher_entry.grid(row=3, column=1)

        published_year_label = tk.Label(add_book_window, text="Published Year: ")
        published_year_label.grid(row=4, column=0)
        published_year_entry = ttk.Entry(add_book_window, width=30)
        published_year_entry.grid(row=4, column=1)

        rating_label = tk.Label(add_book_window, text="Rating: ")
        rating_label.grid(row=5, column=0)
        rating_entry = ttk.Entry(add_book_window, width=30)
        rating_entry.grid(row=5, column=1)

        isbn_label = tk.Label(add_book_window, text="ISBN: ")
        isbn_label.grid(row=6, column=0)
        isbn_entry = ttk.Entry(add_book_window, width=30)
        isbn_entry.grid(row=6, column=1)

        def add_book_to_library():
            """
            Gets multiple entries to create a book instance.
            :return: None
            """
            try:
                title = title_entry.get()
                author = author_entry.get()
                publisher = publisher_entry.get()
                published_year = int(published_year_entry.get())
                rating = float(rating_entry.get())
                isbn = isbn_entry.get()
                if rating > 5 or rating < 1:
                    raise Exception
            except (ValueError, TypeError):
                messagebox.showerror(title="Error!", message="Published year and rating must be entered as number.")
                return
            except Exception:
                messagebox.showerror(title="Error!", message="Rating must be between 1 - 5.")
                return

            if title and author and publisher and published_year and rating and isbn:
                confirm = messagebox.askyesno("Confirmation",
                                              f"""Are you sure you want to add this book?
                                            Title: {title}
                                            Author: {author}
                                            Publisher: {publisher}
                                            Published Year: {published_year}
                                            Rating: {rating}
                                            ISBN: {isbn}    
                                            """)
                if confirm:
                    book = Book(title, author, publisher, published_year, rating, isbn)
                    self.library.add_book(book)
                    messagebox.showinfo("Successful!", "The book has added to the system successfully!")
                    add_book_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        add_button = ttk.Button(add_book_window, text="Add Book", command=add_book_to_library)
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

    def removing_book(self):
        """
        Open a window to remove a book from the library.
        :return: None
        """
        remove_book_window = tk.Toplevel(self.root)
        remove_book_window.title("Remove Book")
        remove_book_window.geometry("500x100")
        remove_book_window.resizable(False, False)

        info_label = tk.Label(remove_book_window, text="Please enter the 'title' of the book you would like to remove:")
        info_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        title_label = tk.Label(remove_book_window, text="Book Title: ")
        title_label.grid(row=1, column=0)
        title_entry = ttk.Entry(remove_book_window, width=30)
        title_entry.grid(row=1, column=1)

        def remove_book_from_library():
            """
            Gets the entry to process next functions argument.
            :return: None
            """
            title = title_entry.get()

            if title:
                confirm = messagebox.askyesno("Confirmation",
                                              "Are you sure you want to remove this book?")
                if confirm:
                    if self.library.remove_book(title):
                        messagebox.showinfo("Successful!", "The book has been removed from the system successfully!")
                        remove_book_window.destroy()
                    else:
                        messagebox.showerror("Error!", "The book cannot be found!")
            else:
                messagebox.showerror("Error", "Please fill in the field.")

        remove_button = ttk.Button(remove_book_window, text="Remove Book", command=remove_book_from_library)
        remove_button.grid(row=2, column=0, columnspan=2, pady=10)

    def adding_member(self):
        """
        Open a window to add a new member to the library.
        :return: None
        """
        add_member_window = tk.Toplevel(self.root)
        add_member_window.title("New Member Information")
        add_member_window.geometry("500x200")
        add_member_window.resizable(False, False)

        info_label = tk.Label(add_member_window, text="Please enter the information of the member: ")
        info_label.grid(row=0, column=0)

        first_name_label = tk.Label(add_member_window, text="First Name: ")
        first_name_label.grid(row=1, column=0)
        first_name_entry = ttk.Entry(add_member_window, width=30)
        first_name_entry.grid(row=1, column=1)

        last_name_label = tk.Label(add_member_window, text="Last Name: ")
        last_name_label.grid(row=2, column=0)
        last_name_entry = ttk.Entry(add_member_window, width=30)
        last_name_entry.grid(row=2, column=1)

        email_label = tk.Label(add_member_window, text="Email: ")
        email_label.grid(row=3, column=0)
        email_entry = ttk.Entry(add_member_window, width=30)
        email_entry.grid(row=3, column=1)

        gender_label = tk.Label(add_member_window, text="Gender: ")
        gender_label.grid(row=4, column=0)
        gender_entry = ttk.Entry(add_member_window, width=30)
        gender_entry.grid(row=4, column=1)

        state_label = tk.Label(add_member_window, text="State: ")
        state_label.grid(row=5, column=0)
        state_entry = ttk.Entry(add_member_window, width=30)
        state_entry.grid(row=5, column=1)

        member_no_label = tk.Label(add_member_window, text="Member No: ")
        member_no_label.grid(row=6, column=0)
        member_no_entry = ttk.Entry(add_member_window, width=30)
        member_no_entry.grid(row=6, column=1)

        def add_member_to_library():
            """
            Gets multiple entries to create a member instance.
            :return: None
            """
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            gender = gender_entry.get()
            state = state_entry.get()
            member_no = member_no_entry.get()

            if first_name and last_name and email and gender and state and member_no:
                confirm = messagebox.askyesno("Confirmation",
                                              f"""Are you sure you want to add this member?
                                            First Name: {first_name}
                                            Last Name: {last_name}
                                            Email: {email}
                                            Gender: {gender}
                                            State: {state}
                                            Member No: {member_no}    
                                            """)
                if confirm:
                    member = Member(first_name, last_name, email, gender, state, member_no)
                    self.library.register_member(member)
                    messagebox.showinfo("Successful!", "The member has registered to the system successfully!")
                    add_member_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        add_button = ttk.Button(add_member_window, text="Add Member", command=add_member_to_library)
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

    def removing_member(self):
        """
        Open a window to remove a member from the library.
        :return: None
        """
        remove_member_window = tk.Toplevel(self.root)

        remove_member_window.title("Remove Member")
        remove_member_window.geometry("500x100")
        remove_member_window.resizable(False, False)
        info_label = tk.Label(remove_member_window,
                              text="Please enter the 'member no' of the member you would like to remove:")

        info_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        member_no_label = tk.Label(remove_member_window, text="Member No: ")

        member_no_label.grid(row=1, column=0)
        member_no_entry = ttk.Entry(remove_member_window, width=30)
        member_no_entry.grid(row=1, column=1)

        def remove_member_from_library():
            """
            Gets the entry to process next functions argument.
            :return: None
            """
            member_no = member_no_entry.get()

            if member_no:
                confirm = messagebox.askyesno("Confirmation",
                                              "Are you sure you want to remove this member?")
                if confirm:
                    if self.library.remove_member(member_no):
                        messagebox.showinfo("Successful!", "The member has been removed from the system successfully!")
                        remove_member_window.destroy()
                    else:
                        messagebox.showerror("Error!", "The member cannot be found!")
            else:
                messagebox.showerror("Error", "Please fill in the field.")

        remove_button = ttk.Button(remove_member_window, text="Remove Member", command=remove_member_from_library)
        remove_button.grid(row=2, column=0, columnspan=2, pady=10)

    def lend_book_process(self):
        """
        Open a window to lend a book to a member.
        :return: None
        """
        lend_book_window = tk.Toplevel(self.root)

        lend_book_window.title("Lend Book Information")
        lend_book_window.geometry("500x200")
        lend_book_window.resizable(False, False)

        info_label = tk.Label(lend_book_window, text="Please enter the 'title' of the book and the 'member no' of the member: ")
        info_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        book_title_label = tk.Label(lend_book_window, text="Book Title: ")
        book_title_label.grid(row=1, column=0)
        book_title_entry = ttk.Entry(lend_book_window, width=30)
        book_title_entry.grid(row=1, column=1)
        member_no_label = tk.Label(lend_book_window, text="Member No: ")

        member_no_label.grid(row=2, column=0)
        member_no_entry = ttk.Entry(lend_book_window, width=30)

        def lend_book_to_member():
            """
            Gets the entries to process next functions arguments.
            :return: None
            """
            book_title = book_title_entry.get()
            member_no = member_no_entry.get()

            if book_title and member_no:
                confirm = messagebox.askyesno("Confirmation",
                                              f"""Are you sure you want to lend this book to this member?
                                            Title: {book_title}
                                            Member No: {member_no}
                                            """)
                if confirm:
                    if self.library.lend_book(title=book_title, member_no=member_no) and self.library.select_one_book(title=book_title):
                        messagebox.showinfo("Successful!", "The book has lent to the member successfully!")
                        lend_book_window.destroy()
                    elif not self.library.select_one_book(title=book_title):
                        messagebox.showerror("Error!", "The book cannot be found.")
                    elif not self.library.select_one_member(member_no):
                        messagebox.showerror("Error!", "The member cannot be found.")
                    else:
                        messagebox.showerror("Error!", "The book is already lent to another member.")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")
        member_no_entry.grid(row=2, column=1)

        add_button = ttk.Button(lend_book_window, text="Lend Book", command=lend_book_to_member)
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

    def return_book_process(self):
        """
        Open a window to return a book to the library.
        :return: None
        """
        return_book_window = tk.Toplevel(self.root)

        return_book_window.title("Lend Book Information")
        return_book_window.geometry("500x200")
        return_book_window.resizable(False, False)
        info_label = tk.Label(return_book_window, text="Please enter the 'title' of the book: ")

        info_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        book_title_label = tk.Label(return_book_window, text="Book Title: ")

        book_title_label.grid(row=1, column=0)
        book_title_entry = ttk.Entry(return_book_window, width=30)
        book_title_entry.grid(row=1, column=1)

        def return_book_to_library():
            """
            Gets the entry to process next functions argument.
            :return: None
            """
            book_title = book_title_entry.get()

            if book_title:
                confirm = messagebox.askyesno("Confirmation",
                                              f"""Are you sure you want to return this book to the library?
                                            Title: {book_title}
                                            """)
                if confirm:
                    if self.library.return_book(title=book_title):
                        messagebox.showinfo("Successful!", "The book has brought back to the library successfully!")
                        return_book_window.destroy()
                    elif self.library.select_one_book(title=book_title):
                        messagebox.showerror("Error!", "The book is already in the library.")
                    else:
                        messagebox.showerror("Error!", "The book cannot be found in the library.")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        add_button = ttk.Button(return_book_window, text="Return Book", command=return_book_to_library)
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

    def add_books_from_csv(self):
        """
        Open a file dialog to add books to the library from a CSV file.
        :return: None
        """
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.library.add_books_from_csv(filename)

    def add_members_from_csv(self):
        """
        Open a file dialog to add members to the library from a CSV file.
        :return: None
        """
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.library.register_members_from_csv(filename)

    def open_html(self, event):
        """
        Open an HTML file in the default web browser.
        :return: None
        """
        script_dir = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join(script_dir, "index.html")
        webbrowser.open_new(html_file_path)

    def exit(self):
        """
        Close the database connection and exit the application.
        :return: None
        """
        self.library.conn.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = LibraryGUI(root)
    app.root.mainloop()


if __name__ == "__main__":
    main()
