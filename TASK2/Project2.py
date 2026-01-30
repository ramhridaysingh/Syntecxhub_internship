            #Project 2 : Library Book Inventory Manager


#Book class to represent each book in the inventory

class Book:
    def __init__(self, book_id, title, author):
        self.id = book_id
        self.title = title
        self.author = author
        self.issued = False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }

#Library class to manage the book inventory
import json
import os

class Library:
    FILE_NAME = "library.json"

    def __init__(self):
        self.books = self.load_books()   # dict → quick lookup

    def load_books(self):
        if os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "r") as file:
                return json.load(file)
        return {}

    def save_books(self):
        with open(self.FILE_NAME, "w") as file:
            json.dump(self.books, file, indent=4)

    def add_book(self, book):
        if book.id in self.books:
            print("❌ Book ID already exists.")
            return
        self.books[book.id] = book.to_dict()
        self.save_books()
        print("✅ Book added successfully.")

    def search_book(self, keyword):
        found = False
        for book in self.books.values():
            if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower():
                print(f"ID: {book['id']} | {book['title']} by {book['author']} | Issued: {book['issued']}")
                found = True
        if not found:
            print("No matching books found.")

    def issue_book(self, book_id):
        if book_id in self.books and not self.books[book_id]["issued"]:
            self.books[book_id]["issued"] = True
            self.save_books()
            print("📕 Book issued successfully.")
        else:
            print("❌ Book not available or not found.")

    def return_book(self, book_id):
        if book_id in self.books and self.books[book_id]["issued"]:
            self.books[book_id]["issued"] = False
            self.save_books()
            print("📗 Book returned successfully.")
        else:
            print("❌ Book not issued or not found.")

    def report(self):
        total = len(self.books)
        issued = sum(1 for b in self.books.values() if b["issued"])
        print("\n--- Library Report ---")
        print(f"Total Books : {total}")
        print(f"Issued Books: {issued}")

#Main function to interact with the user
def main():
    library = Library()

    while True:
        print("\n--- Library Book Inventory Manager ---")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Report")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            bid = input("Enter Book ID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            book = Book(bid, title, author)
            library.add_book(book)

        elif choice == "2":
            keyword = input("Enter title or author to search: ")
            library.search_book(keyword)

        elif choice == "3":
            bid = input("Enter Book ID to issue: ")
            library.issue_book(bid)

        elif choice == "4":
            bid = input("Enter Book ID to return: ")
            library.return_book(bid)

        elif choice == "5":
            library.report()

        elif choice == "6":
            print("Goodbye 👋")
            break

        else:
            print("Invalid choice. Try again.")


# Run program
main()
