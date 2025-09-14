import logging
from fastapi import UploadFile

from app.config import settings
from app.db.connection import get_supabase


logger = logging.getLogger(__name__)


class BookService:
    """Service class for handling book related operations."""
    
    def __init__(self):
        self.supabase = get_supabase()
    
    async def upload_pdf(
        self, 
        user_id: str,
        book_pdf: UploadFile,
        subject: str,
        class_level: str,
        is_public: bool = True
    ):
        """Upload a pdf book to supabase storage and save book metadata to supabase table."""
        
        try:
            
            bucket = self.supabase.storage.from_(settings.supabase_bucket)
            file_content = await book_pdf.read()
            file_path = f"/{class_level}/{subject}.pdf"
            
            bucket.upload(
                file=file_content,
                path=file_path,
                # path=book_title
                file_options={"content-type": "application/pdf"}
            )
            
            pdf_url = bucket.get_public_url(file_path)
            
            data = {
                "class_level": class_level,
                "subject": subject,
                "title": book_pdf.filename,
                "supabase_path": file_path,
                "pdf_url": pdf_url,
                "is_public": is_public,
                "uploaded_by": user_id,
            }
            
            response = self.supabase.table("books").insert(data).execute()
            return response.data
        
        except Exception as e:
            logger.error(f"Error upload pdf book to supabase: {e}")
            raise e


