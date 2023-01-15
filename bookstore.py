import sqlite3
from tabulate import tabulate

# Creating a database named ebook store
db = sqlite3.connect(':memory:')
c = db.cursor()

# Creating a table named books
c.execute('''CREATE TABLE books
        (id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)''')
db.commit()


# Creating a book class that includes methods for updating a book
class Book:
    def __init__(self, book_id, book_title, book_auth, book_qty):
        self.id = book_id
        self.title = book_title
        self.auth = book_auth
        self.qty = book_qty

    def update_id(self, new_id):
        c.execute('''UPDATE books SET id = ? WHERE id = ?''', (new_id,
                                                               self.id))
        db.commit()
        self.id = new_id
        return self.id

    def update_title(self, new_title):
        self.title = new_title
        c.execute('''UPDATE books SET Title = ? WHERE id = ?''', (new_title,
                                                                  self.id))
        db.commit()
        return self.title

    def update_auth(self, new_auth):
        c.execute('''UPDATE books SET Author = ? WHERE id = ?''', (new_auth,
                                                                   self.id))
        db.commit()
        self.auth = new_auth
        return self.auth

    def update_qty(self, new_qty):
        c.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (new_qty,
                                                                self.id))
        db.commit()
        self.qty = new_qty
        return self.qty

    def attributes(self):
        return self.id, self.title, self.auth, self.qty


# Creating functions
def show_menu():
    """
    This function presents the user with the main menu and takes the user's
    number choice for the menu option. Includes handling value error.
    :return: int representing user's menu option choice
    """
    while True:
        print("""
Please choose one of the following options (0-4):
    1 => Enter book
    2 => Update book
    3 => Delete book
    4 => Search books
    0 => Exit""")
        try:
            menu_input = int(input("==> "))
            return menu_input
            break
        except ValueError:
            print(
                "Invalid option. Please enter a number between 1 and 4, "
                "or 0 to exit.")


def show_update_menu():
    """
    This function presents the user with the update option menu and takes the
    user's number choice for the update option. Includes handling value error.
    :return: int representing user's update menu choice
    """
    while True:
        print("""What would you like to update? 
        1 => Book's id
        2 => Book's Title
        3 => Book's Author
        4 => Book's Quantity
        0 => Return to main menu""")

        try:
            update_menu = int(input("==> "))
            break
        except ValueError:
            print(
                "Invalid entry. Please enter a number between 1 and 4, "
                "or 0 to exit.")
    return update_menu


def enter_book():
    """
    This function takes details about a new book (id, title, author and
    quantity and creates a Book() object and inserts this book into the book
    database.
    Includes value error handling
    :return: str representing success message
    """
    while True:
        try:
            book_id_input = int(input("Book id: "))
            c.execute('''SELECT  * FROM books where ID = ?''',
                      (book_id_input,))
            res1 = c.fetchall()
            if res1:
                print("This id already exists, please ensure you enter an "
                      "unique id")
                continue
            break
        except ValueError:
            print("Invalid id, please try again using numbers!")
    book_title = input("Book title: ")
    book_auth = input("Book author: ")
    while True:
        try:
            book_qty = int(input("Book quantity: "))
            break
        except ValueError:
            print("Please enter a number!")
    new_book = Book(book_id_input, book_title, book_auth, book_qty)
    c.execute('''INSERT into books(id, Title, Author, Qty)
                VALUES (?, ?, ?, ?)''', new_book.attributes())
    return f'\nBook "{book_title}" by {book_auth} successfully added!'


def show_books_table():
    """
    This function selects all the books in the database and prints this info
    in a user-friendly table. Used to give the user an overview of what is
    currently in the database.
    :return: N/A
    """
    c.execute('''SELECT  * FROM books''')
    res1 = c.fetchall()

    books_list = []
    for book in res1:
        book = [item for item in book]
        books_list.append(book)

    print(tabulate(books_list,
                   headers=["Book ID", "Book Title", "Author", "Quantity"],
                   tablefmt="grid"))


def get_book_to_update():
    """
    This function will get the book that will be updated, according to the id
    that user in inputting. Handles value error as well as checks if the id
    is valid (if book with this id exists in the current database)
    :return: object representing the book that is to be updated
    """
    c.execute('''SELECT  * FROM books''')
    books = c.fetchall()
    book_to_update = None
    while True:
        try:
            book_id = int(input("Insert the book id for the book you "
                                "would like to update: "))
            id_list = []
            for book in books:
                id_list.append(book[0])
                if book_id in id_list and book[0] == book_id:
                    book_to_update = Book(book[0], book[1], book[2],
                                          book[3])
            if book_to_update is None:
                print("Invalid id, please try again.")
                continue
            break
        except ValueError:
            print("Invalid id, please try again.")
    return book_to_update


def get_book_to_delete():
    """
    This function will get the id of the book to be deleted, according to the
    using user input. Handles value error as well as checks if the id
    is valid (if book with this id exists in the current database)
    :return: int representing the id of the book to be deleted
    """
    c.execute('''SELECT  * FROM books''')
    books = c.fetchall()
    while True:
        try:
            book_id = int(input("Insert the book id for the book you "
                                "would like to delete: "))
            id_list = []
            for book in books:
                id_list.append(book[0])

            if book_id not in id_list:
                print("Invalid id, please try again.")
                continue
            break
        except ValueError:
            print("Invalid id, please try again.")
    return book_id


def search_book():
    """
    This function takes the parameter by which a book will be searched. If the
    input is a valid parameter, the function will search for the book matching
    this parameter in the database and print the search results in a table
    format. Includes checks for valid parameters and valid parameter values.
    :return:
    """
    search_by = input('Search By (id/title/author): ').strip()
    search_details = input(f'Search by {search_by} details: ')
    if search_by.lower() in ["id", "title", "author"]:
        c.execute(f"SELECT * FROM books where {search_by} LIKE ? OR "
                  f"{search_by} LIKE ?", (search_details,
                                          f'%{search_details}%'))
        search_result = c.fetchall()
        if search_result:
            print("\nHere is what I found:")
            print(tabulate([book for book in search_result],
                           headers=["Book ID", "Book Title", "Author",
                                    "Quantity"],
                           tablefmt="grid"))
        else:
            print(f'Sorry, there is no book with {search_by} of '
                  f'"{search_details}"')
    else:
        print("Invalid search criteria. Please try again.")


# Populating the table with values using object created via Book() class
books = [Book(3001, "A Tale of Two Cities", "Charles Dickens", 30),
         Book(3002, "Harry Potter and the Philosopher's Stone",
              "J. K. Rowling", 40),
         Book(3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
         Book(3004, "The Lord of the Rings", "J. R. R. Tolkien", 37),
         Book(3005, "Alice in Wonderland", "Lewis Carroll", 12)]

c.executemany('''INSERT into books(id, Title, Author, Qty)
                VALUES (?, ?, ?, ?)''', [book.attributes() for book in books])
db.commit()

# User menu
print("""
Welcome to your ebook store manager system""")

while True:
    menu = show_menu()

    if menu == 0:
        print("Goodbye!")
        exit()

    elif menu == 1:
        print("Enter Book Menu")
        print(enter_book())
        print("\nHere are all the books: ")
        show_books_table()

    elif menu == 2:
        print("Update Book Menu")
        print("\nHere are all the books: ")
        show_books_table()
        book_to_update = get_book_to_update()
        update_menu = show_update_menu()

        # Handling the update menu choice
        # Using Book() class methods to update id, title, auth and qty
        if update_menu == 0:
            continue
        elif update_menu == 1:
            new_id = int(input("New id: "))
            book_to_update.update_id(new_id)
            print(f"Id for '{book_to_update.title}' successfully updated"
                  f" to {new_id}. ")
        elif update_menu == 2:
            new_title = input("New title: ")
            book_to_update.update_title(new_title)
            print(f"Title successfully updated to {new_title}.")
        elif update_menu == 3:
            new_auth = input("New author: ")
            book_to_update.update_auth(new_auth)
            print(f"Author for '{book_to_update.title}' successfully updated"
                  f" to {new_auth}. ")
        elif update_menu == 4:
            new_qty = int(input("New quantity: "))
            book_to_update.update_qty(new_qty)
            print(f"Quantity for '{book_to_update.title}' successfully updated"
                  f" to {new_qty}. ")
        else:
            print("Invalid entry, please try again.")

    elif menu == 3:
        print("Delete Book Menu")
        print("\nHere are all the books: ")
        show_books_table()
        book_id = get_book_to_delete()
        c.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
        db.commit()
        print(f"Book with id '{book_id}' successfully deleted.")

    elif menu == 4:
        print("Search Book Menu")
        search_book()

    else:
        print("Invalid option. Please enter a number between 1 and 4, or 0 to "
              "exit.")
