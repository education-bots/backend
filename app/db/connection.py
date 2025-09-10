import logging
from typing import Optional
from fastapi.concurrency import asynccontextmanager
from pinecone import Pinecone, ServerlessSpec
from pinecone.db_data.index import Index
from supabase import Client, create_client

from app.config import settings


logger = logging.getLogger(__name__)

# GLobal clients
supabase_client: Optional[Client] = None
pinecone_client: Optional[Pinecone] = None
pinecone_index = None


async def initialize_supabase() -> Client:
    """Initialize Supabase client"""
    try:
        client = create_client(settings.supabase_url, settings.supabase_key)
        logger.info("Supabase client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        raise e



async def initialize_pinecone() -> tuple[Pinecone, Index]:
    """Initialize Pinecone client and index"""
    try:
        pc = Pinecone(api_key=settings.pinecone_api_key)
        
        # Check if index exists, create if not
        if settings.pinecone_index not in pc.list_indexes().names():
            pc.create_index(
                name=settings.pinecone_index,
                dimension=settings.embedding_dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=settings.pinecone_environment
                )
            )
            logger.info(f"Created Pinecone index: {settings.pinecone_index}")
            
        
        index = pc.Index(settings.pinecone_index)
        return pc, index
    except Exception as e:
        logger.error(f"Failed to initialize Pinecone: {e}")
        raise e

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
    global supabase_client, pinecone_client, pinecone_index
    
    logger.info("Starting up application...")
    
    try:
        # Initialize all services
        supabase_client = await initialize_supabase()
        pinecone_client, pinecone_index = await initialize_pinecone()
        await initialize_mcp_server()
        
        logger.info("All services initialized successfully")
        yield

    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise e
    
    finally:
        supabase_client = None
        pinecone_client = None    
        pinecone_index = None    
        logger.info("Shutting down application...")


def get_supabase() -> Client:
    """Get Supabase client"""
    if supabase_client is None:
        raise RuntimeError("Supabase client not initialized")
    return supabase_client


def get_pinecone_index():
    """Get Pinecone index"""
    if pinecone_index is None:
        raise RuntimeError("Pinecone index not initialized")
    return pinecone_index


def get_pinecone_client() -> Pinecone:
    """Get Pinecone client"""
    if pinecone_client is None:
        raise RuntimeError("Pinecone client not initialized")
    return pinecone_client

