from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Book(BaseModel):
    id: str = Field(..., description="Unique identifier for the book")
    title: str = Field(..., description="Title of the book")
    author: str = Field(..., description="Author of the book")
    published_date: datetime = Field(..., description="Date the book was published")
    isbn: str = Field(..., description="International Standard Book Number")
    pages: int = Field(..., description="Number of pages in the book")
    language: str = Field(..., description="Language of the book")
    publisher: str = Field(..., description="Publishing company")
    genre: Optional[str] = Field(None, description="Genre of the book")
    rating: Optional[float] = Field(None, description="Average rating of the book")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "book_123",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "published_date": "1925-04-10T00:00:00",
                "isbn": "9780743273565",
                "pages": 218,
                "language": "en",
                "publisher": "Charles Scribner's Sons",
                "genre": "Classic",
                "rating": 4.5
            }
        }
