import os
from config import db
from models import User, Book

BOOKS = [
    {"title": "Sweet Thursday", "author": "John Steinbeck","publisher": "New Horizon","description": "It is a sequel to Cannery Row","amount": 1},
    {"title": "For Whom the Bell Tolls", "author": "Ernest Hemingway","publisher": "Oxford","description": "describes the brutality of the Spanish Civil War","amount": 1},
    {"title": "Not A Science", "author": "Unknown Hero","publisher": "One Day","description": "A Science Fiction","amount": 1}
]

# Delete database file if it exists currently
if os.path.exists("books.db"):
    os.remove("books.db")
    
# Create the database
db.create_all()

# iterate over the BOOKS structure and populate the database

for book in BOOKS:
    p = Book(title=book.get("title"), author=book.get("author"), publisher=book.get("publisher"), description=book.get("description"), amount=book.get("amount"))
    db.session.add(p)

db.session.commit()
