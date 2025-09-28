from openai import AsyncOpenAI
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from agents import set_default_openai_client, set_default_openai_api, set_tracing_disabled
 
load_dotenv()
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT")
class Settings(BaseSettings):
    
    # API Configuration
    app_name: str = "AI Learning Platform"
    debug: bool = False
    
    # Authentication
    frontend_auth_header: str = "edu-api-client"
    frontend_auth_secret: str
    
    # Gemini API
    gemini_api_key: str
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    
    # Supabase Configuration
    supabase_url: str
    supabase_key: str
    supabase_bucket: str = "books"

    # Front-end deployed url
    frontend_url: str

    # MCP Server Configuration
    mcp_server_port: int = 8001

    def initialize_gemini_model(self):
        gemini_client = AsyncOpenAI(api_key=self.gemini_api_key, base_url=self.gemini_base_url)
        set_default_openai_client(gemini_client)
        set_default_openai_api("chat_completions")
        set_tracing_disabled(disabled=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Required environment variable '{var_name}' is not set.")
    return value

settings = Settings()
settings.initialize_gemini_model()

