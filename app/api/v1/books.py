import logging
from fastapi import APIRouter, Depends, HTTPException

from app.core.security import verify_auth_header
from app.db.connection import get_supabase
from app.schemas.book_schema import BookRequest
from app.services.books_service import BookService


logger = logging.getLogger(__name__)
router = APIRouter()



@router.post("/upload")
async def upload_book(request: BookRequest, _: str = Depends(verify_auth_header)):
    """Upload a book in pdf"""
    
    print(request)
    
    try:
        # Check if user is admin
        supabase = get_supabase()
        result = (
            supabase
            .table("profiles")
            .select('role')
            .eq('id', request.user_id)
            .eq('role', 'admin')
            .execute()
        )
        
        if not result.data:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )

        if request.book_pdf.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Invalid file format"
            )

        books_service = BookService()
        response = await books_service.upload_pdf(
            book_pdf = request.book_pdf,
            user_id = str(request.user_id),
            subject = request.subject,
            class_level = request.class_level,
            is_public = request.is_public
        )

        return response


    except Exception as e:
        logger.error(f"Error processing agent request: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing request"
        )

