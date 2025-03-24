from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from models import Book

class MongoDBClient:
    def __init__(self, uri: str):
        """
        Initialize MongoDB client
        
        Args:
            uri: MongoDB connection URI
        """
        self.client = MongoClient(uri)
        self.db = self.client['books_db']
        self.books: Collection = self.db['books']
        
        # Create unique index on book id
        self.books.create_index("id", unique=True)

    def save_book(self, book: Book) -> bool:
        """
        Save a book document to MongoDB
        
        Args:
            book: Book model instance
            
        Returns:
            bool: True if successful, False if duplicate
        """
        try:
            self.books.insert_one(book.model_dump())
            return True
        except DuplicateKeyError:
            return False

    def get_book(self, book_id: str) -> Optional[Book]:
        """
        Get a book by its ID
        
        Args:
            book_id: Unique identifier of the book
            
        Returns:
            Optional[Book]: Book object if found, None otherwise
        """
        book_data = self.books.find_one({"id": book_id})
        return Book(**book_data) if book_data else None

    def update_book(self, book_id: str, book: Book) -> bool:
        """
        Update an existing book
        
        Args:
            book_id: Unique identifier of the book
            book: Updated book data
            
        Returns:
            bool: True if successful, False if not found
        """
        result = self.books.update_one(
            {"id": book_id},
            {"$set": book.model_dump()}
        )
        return result.modified_count > 0

    def delete_book(self, book_id: str) -> bool:
        """
        Delete a book by its ID
        
        Args:
            book_id: Unique identifier of the book
            
        Returns:
            bool: True if successful, False if not found
        """
        result = self.books.delete_one({"id": book_id})
        return result.deleted_count > 0
