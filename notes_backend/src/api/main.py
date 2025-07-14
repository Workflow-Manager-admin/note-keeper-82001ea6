from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment
load_dotenv()

from .db import init_db
from . import routes

# Metadata for OpenAPI schema
tags_metadata = [
    {"name": "Auth", "description": "User registration and authentication."},
    {"name": "Notes", "description": "Create, view, update and delete notes."},
]

app = FastAPI(
    title="Notes Backend API",
    description="Backend API to manage notes operations, user authentication, and data retrieval.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB if required
init_db()

# Register routes
app.include_router(routes.router)

@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Returns API health status."""
    return {"message": "Healthy"}
