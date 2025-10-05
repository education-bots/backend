from fastapi import FastAPI

from app.config import settings
from app.db.connection import lifespan
from app.api.v1.agent import router as agent_router
from app.api.v1.books import router as books_router
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.app_name,
        description="AI-powered learning platform for rural children (K-4)",
        version="1.0.0",
        lifespan=lifespan,
        debug=settings.debug
    )
    
    # Include routers
    app.include_router(agent_router, prefix="/api/v1/agents")
    app.include_router(books_router, prefix="/api/v1/books")
    
    origins = [
        "http://localhost:3000",
        settings.frontend_url,
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,  # Allow cookies and authentication headers
        allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],     # Allow all headers
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": settings.app_name}
    
    return app


# Create the app instance
app = create_app()

@app.get("/")
async def home():
    return {"message": "Welcome to AI-powered learning platform for rural children (K-4).\nVisit '/docs' for more information"}


