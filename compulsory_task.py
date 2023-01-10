import sqlite3
from tabulate import tabulate
import tkinter as tk
import os

db = sqlite3.connect('ebookstore_db')
cursor = db.cursor()  # Get a cursor object

try:    # creates table if it doesn't exist
    cursor.execute("CREATE TABLE books(id TEXT PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)") 
except:
    pass


class MainMenu(tk.Tk):  # each instance of class has six buttons, each of which calls one of the functions
    def __init__(self):
        super().__init__()
        
        self.button1 = tk.Button(self, text="View all", command=display_all)
        self.button2 = tk.Button(self, text="Enter book", command=add_book)
        self.button3 = tk.Button(self, text="Update book", command=update_book)
        self.button4 = tk.Button(self, text="Delete book", command=delete_book)
        self.button5 = tk.Button(self, text="Search books", command=search_books)
        self.button6 = tk.Button(self, text="Exit", command=close_program)

        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.button4.pack()
        self.button5.pack()
        self.button6.pack()


class EditMenu(tk.Tk):  # each instance of class has three buttons, each of which calls one of the functions
    def __init__(self):
        super().__init__()
        
        self.button1 = tk.Button(self, text="Update title", command=update_title)
        self.button2 = tk.Button(self, text="Update author", command=update_author)
        self.button3 = tk.Button(self, text="Update quantity", command=update_quantity)

        self.button1.pack()
        self.button2.pack()
        self.button3.pack()


def confirm_yesno():

    confirm = ""
    while confirm != "y" or confirm != "n":

        confirm = input("Are you sure? (y/n): ").lower()

        if confirm != "y" and confirm != "n":

            print("Input not recognised.")
        
        else:

            return confirm

def check_id(id):   # checks if id entered by user is in use

    cursor.execute("SELECT id FROM books")
    result = cursor.fetchall()
    id_list = [row[0] for row in result]
    if id in id_list:
        return "That id is currently in use."


def get_id():   # requests book id from user

    while True:

        id = input("Enter the book's unique id: ")
        check = check_id(id)
        
        if check == None:
            break
        else:
            print(check)
    
    return id


def get_quantity(): # requests quantity from user, ensuring correct value

    while True:

        try:
            quantity = int(input("Enter the quantity: "))

            if quantity < 0:
                print("Quantity must be positive.")
            else:
                break

        except ValueError:
            print("Quantity must be a positive integer.")
    
    return quantity


def add_book(): # requests values from user and adds to database

    window.destroy()    # removes menu window

    print("Enter the details of the book you would like to add to the system \n")
    
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    
    quantity = get_quantity()
    
    id = get_id()

    cursor.execute("INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)", (id, title, author, quantity))
    print("\nBook successfully added to database.")

    db.commit()


def update_book():  # allows user to update info for book

    window.destroy()

    global id
    id = input("Enter the id of the book for which you would like to edit the information: ")

    check = check_id(id)    # ensures user has entered the id for a book that exists in the database

    if check == None:

        print("The id that has been entered does not correspond to any book in the database.")
    
    else:
        
        global window2
        window2 = EditMenu()    # creates an instance of the menu for calling one of the functions for editing book info
        window2.title("Would you like to update title, author, or quantity?")
        window2.mainloop()


def update_title(): # updates the title of the book

    window2.destroy()

    title = input("Enter the name of the book: ")

    cursor.execute("UPDATE books SET Title = ? WHERE id = ?", (title, id))

    db.commit()


def update_author():    # updates the author of the book

    window2.destroy()

    author = input("Enter the name of the author: ")

    cursor.execute("UPDATE books SET Author = ? WHERE id = ?", (author, id))

    db.commit()


def update_quantity():  # updates the quantity of the book

    window2.destroy()

    quantity = get_quantity()

    cursor.execute("UPDATE books SET Qty = ? WHERE id = ?", (quantity, id))

    db.commit()


def search_books(): # checks if any record in the database matches the title entered by the user

    window.destroy()

    title = input("Enter the title of the book you would like to check: ")

    cursor.execute("SELECT Title FROM books")
    result = cursor.fetchall()
    title_list = [row[0] for row in result] # creates list that stores all the book titles
    if title in title_list: # if the user input is in the list, the correspondng record is diplayed

        print("That book is in the database.")

        cursor.execute("SELECT * FROM books WHERE Title IN (?)", (title,))

        info = cursor.fetchall()

        print(tabulate(info, headers=['id', 'Title', 'Author', 'Qty'], tablefmt='grid'))

    else:

        print("That book is not in the database.")


def delete_book():  # removes a record from the database

    window.destroy()

    id = input("Enter the id of the book you would like to delete: ")

    check = check_id(id)    # checks if user input matches any existing id

    if check == None:

        print("The id that has been entered does not correspond to any book in the database.")
    
    else:

        confirm = confirm_yesno()   # asks for confirmation before deleting record

        if confirm == "y":

            cursor.execute("DELETE FROM books WHERE id IN (?)", (id,))
            print("Book deleted.")
            db.commit()
        
        else:

            print("Book not deleted.")
        

def display_all():  # shows entire table

    window.destroy()

    cursor.execute("SELECT * FROM books ORDER BY id")

    info = cursor.fetchall()

    print(tabulate(info, headers=['id', 'Title', 'Author', 'Qty'], tablefmt='grid'))


def close_program():

    db.close()

    exit()


while True:

    window = MainMenu() # creates instance of menu window
    window.title("Select an option:")
    print("Select an option from the menu")
    window.mainloop()   # opens menu window

    enter_continue = input("Press enter to continue")
    os.system('cls')    # clears screen so that information is always displayed at the top