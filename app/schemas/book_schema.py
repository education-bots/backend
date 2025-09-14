from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import UploadFile


class BookRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user asking the question")
    book_pdf: UploadFile = Field(..., description="Book in PDF format.")
    subject: str = Field(..., description="Language of the book")
    class_level: str = Field(..., description="Class level of the book")
    is_public: bool = Field(..., description="Weather keep book public or not")
    
    