
# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="My Awesome FastAPI Project",
    description="This is a boilerplate for a FastAPI project.",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Configuration ---
# You can load configurations from a separate config file or environment variables
# For example:
# from app.core.config import settings
# app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


# --- Middleware ---
# CORS Middleware: Allows cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"],  # Allows all headers
)

# Other middleware can be added here, e.g., for authentication, logging, etc.
# from app.middleware.auth import AuthMiddleware
# app.add_middleware(AuthMiddleware)


# --- Routers ---
# Include your API routers here.
# For example, if you have a 'users' module with a router:
# from app.api.v1.endpoints import users
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

# A simple root endpoint for demonstration
@app.get("/", summary="Root endpoint", response_description="Returns a welcome message.")
async def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to My Awesome FastAPI Project!"}


# --- Dependencies ---
# Global dependencies can be defined here, e.g., database session
# from app.dependencies import get_db
# @app.get("/items/", dependencies=[Depends(get_db)])
# async def read_items():
#     return [{"item_id": "Foo"}]


# --- Event Handlers ---
# Startup event handler
@app.on_event("startup")
async def startup_event():
    print("Application startup event triggered.")
    # Initialize database connections, load models, etc.
    # For example: await database.connect()

# Shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutdown event triggered.")
    # Close database connections, clean up resources, etc.
    # For example: await database.disconnect()


# --- Run the application using Uvicorn ---
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reloads the server on code changes (for development)
        log_level="info",
    )
