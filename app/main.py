from fastapi import FastAPI

from app.config import settings
from app.db.connection import lifespan
from app.api.v1.agent import router as agent_router

 


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

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": settings.app_name}
    
    return app


# Create the app instance
app = create_app()

@app.get("/")
async def home():
    return {"message": "Welcome to AI-powered learning platform for rural children (K-4).\nVisit '\\docs' for more information"}


