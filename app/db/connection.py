import logging
from typing import Optional
from fastapi.concurrency import asynccontextmanager
from sentence_transformers import SentenceTransformer
from supabase import Client, create_client

from app.config import settings


logger = logging.getLogger(__name__)

# GLobal clients
supabase_client: Optional[Client] = None
supabase_embedding_model: Optional[SentenceTransformer] = None

# Load the gte-small model
# model = SentenceTransformer('Supabase/gte-small')


async def initialize_supabase() -> Client:
    """Initialize Supabase client"""
    try:
        client = create_client(settings.supabase_url, settings.supabase_key)
        logger.info("Supabase client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        raise Exception from e


async def initialize_embedding_model() -> SentenceTransformer:
    """Initialize Supabase Embedding Model"""
    try:
        supabase_embedding_model = SentenceTransformer('Supabase/gte-small')
        logger.info("Supabase client initialized successfully")
        return supabase_embedding_model
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client {e}")
        raise Exception from e


async def initialize_mcp_server():
    """Initialize Supabase MCP server"""
    try:
        # This would be where the MCP server will start
        # For now, we'll just log that it would be initialized
        logger.info("MCP server would be initialized here")
        # TODO: Implement actual MCP server startup
    except Exception as e:
        logger.error(f"Failed to initialize MCP server: {e}")
        raise




@asynccontextmanager
async def lifespan(app):
    """Application lifespan manager"""
    global supabase_client, supabase_embedding_model
    
    logger.info("Starting up application...")
    
    try:
        # Initialize all services
        supabase_client = await initialize_supabase()
        print("initialize_embedding_model")
        supabase_embedding_model = await initialize_embedding_model()
        await initialize_mcp_server()
        
        logger.info("All services initialized successfully")
        yield

    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise Exception from e
    
    finally:
        supabase_client = None
        supabase_embedding_model = None
        logger.info("Shutting down application...")


def get_supabase() -> Client:
    """Get Supabase client"""
    if supabase_client is None:
        raise RuntimeError("Supabase client not initialized")
    return supabase_client

def get_supabase_embedding_model() -> SentenceTransformer:
    """Get Supabase embedding model"""
    if supabase_embedding_model is None:
        raise RuntimeError("Supabase embedding model not initialized")
    return supabase_embedding_model

