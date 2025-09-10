# AI Learning Platform Backend

An AI-powered learning platform backend designed for rural children (K-4) using FastAPI, OpenAI Agents, and modern AI technologies.

## 📁 Project Structure

This document outlines the folder structure to help contributors understand the codebase organization and where to place new features.

```
backend-test/
├── 📁 app/                          # Main application package
│   ├── 📄 __init__.py              # Package initialization
│   ├── 📄 main.py                  # FastAPI application entry point
│   ├── 📄 config.py                # Application configuration & settings
│   │
│   ├── 📁 api/                     # API layer - HTTP endpoints
│   │   ├── 📄 __init__.py
│   │   └── 📁 v1/                  # API version 1
│   │       ├── 📄 __init__.py
│   │       └── 📄 agent.py         # Agent-related endpoints
│   │
│   ├── 📁 agents/                  # AI Agent implementations
│   │   ├── 📄 __init__.py
│   │   ├── 📄 helpper.py           # Agent helper utilities
│   │   ├── 📄 test_agent.py        # Agent testing utilities
│   │   └── 📁 memory/              # Agent memory management
│   │       └── 📄 __init__.py
│   │
│   ├── 📁 core/                    # Core application logic
│   │   └── 📄 security.py          # Security utilities & middleware
│   │
│   ├── 📁 db/                      # Database layer
│   │   └── 📄 connection.py        # Database connection & session management
│   │
│   ├── 📁 schemas/                 # Pydantic models & data validation
│   │   ├── 📄 agent_schema.py      # Agent-related data models
│   │   └── 📄 user_schema.py       # User-related data models
│   │
│   └── 📁 services/                # Business logic layer
│       └── 📄 agent_service.py     # Agent business logic
│
├── 📄 pyproject.toml               # Project dependencies & metadata
├── 📄 uv.lock                      # Dependency lock file
└── 📄 README.md                    # This file
```

## 🏗️ Architecture Overview

### Layer Structure
- **API Layer** (`app/api/`): HTTP endpoints, request/response handling
- **Service Layer** (`app/services/`): Business logic, data processing
- **Data Layer** (`app/db/`, `app/schemas/`): Database operations, data models
- **Core Layer** (`app/core/`): Shared utilities, security, middleware
- **Agent Layer** (`app/agents/`): AI agent implementations and memory

### Technology Stack
- **Framework**: FastAPI
- **AI/ML**: OpenAI Agents, Gemini API
- **Database**: Supabase
- **Vector Database**: Pinecone
- **Package Manager**: uv
- **Python Version**: 3.12+

## 📝 Where to Add New Features

### Adding New API Endpoints
```
app/api/v1/
├── agent.py          # Existing agent endpoints
├── user.py           # Add user management endpoints
├── content.py        # Add educational content endpoints
└── analytics.py      # Add analytics endpoints
```

### Adding New Services
```
app/services/
├── agent_service.py      # Existing agent service
├── user_service.py       # Add user management logic
├── content_service.py    # Add content management logic
└── analytics_service.py  # Add analytics logic
```

### Adding New Data Models
```
app/schemas/
├── agent_schema.py       # Existing agent schemas
├── user_schema.py        # Existing user schemas
├── content_schema.py     # Add content-related schemas
└── analytics_schema.py   # Add analytics schemas
```

### Adding New AI Agents
```
app/agents/
├── helpper.py            # Existing helper utilities
├── test_agent.py         # Existing test agent
├── tutor_agent.py        # Add tutoring agent
├── assessment_agent.py   # Add assessment agent
└── memory/               # Agent memory management
    └── __init__.py      # Add long-term memory
```

## 🚀 Getting Started for Contributors

### Prerequisites
- Python 3.12+
- uv package manager
- Access to required API keys (Gemini, Supabase, Pinecone)

### Setup Instructions
1. Clone the repository
2. Install dependencies: `uv sync`
3. Create `.env` file with required environment variables
4. Run the application: `uv run uvicorn app.main:app --reload`

### Environment Variables
Create a `.env` file with:
```bash
# Authentication
FRONTEND_AUTH_SECRET="your-secret"

# Gemini API
GEMINI_API_KEY="your-gemini-key"

# Supabase
SUPABASE_URL="your-supabase-url"
SUPABASE_KEY="your-supabase-key"
SUPABASE_BUCKET="books"

# Pinecone
PINECONE_API_KEY="your-pinecone-key"
PINECONE_INDEX="your-index-name"
PINECONE_ENVIRONMENT="us-east-1"

# MCP Server
MCP_SERVER_PORT=8001
```

## 📋 Development Guidelines

### Code Organization
- Follow the existing layer separation (API → Service → Data)
- Keep business logic in services, not in API endpoints
- Use Pydantic schemas for data validation
- Place shared utilities in the `core/` directory

### Naming Conventions
- Use snake_case for file and function names
- Use PascalCase for class names
- Use descriptive names that indicate purpose

### Adding Dependencies
- Add new dependencies to `pyproject.toml`
- Run `uv lock` to update the lock file
- Document any new dependencies in this README

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI Agents Documentation](https://github.com/openai/agents)
- [Supabase Documentation](https://supabase.com/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)

---

**Note**: This structure is designed to be scalable and maintainable. When adding new features, follow the existing patterns and maintain separation of concerns.
