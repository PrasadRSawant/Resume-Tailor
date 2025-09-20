
# app/main.py
# Application entry point. Initializes FastAPI app, includes routers, sets up middleware, dependencies, and configurations. Runs server using Uvicorn.

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from uvicorn import Config, Server
from logging.config import dictConfig
import logging

# Assuming these modules exist in your project structure
# from app.core.config import settings  # For centralized configuration
# from app.core.logging import log_config # For logging configuration
# from app.routers import user, item    # Example routers

# Basic logging configuration (replace with app.core.logging.log_config if available)
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO"
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        }
    }
}
dictConfig(log_config)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title='My FastAPI Project',
    description='This is a professional and scalable FastAPI project setup.',
    version='1.0.0',
    contact={
        'name': 'Your Name',
        'email': 'your.email@example.com',
    },
    license_info={
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT',
    },
    docs_url='/docs',
    redoc_url='/redoc'
)

# Set up CORS middleware
# In a real application, origins should be loaded from app.core.config.settings.CORS_ORIGINS
# For now, we use a simple placeholder.
origins = ["http://localhost", "http://localhost:8000", "http://127.0.0.1:8000"] # Example origins
# If using app.core.config.settings, it would be: origins = settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
# You would define your routers in app/routers/ and then include them here.
# Example:
# from app.routers import user, item
# app.include_router(user.router, prefix='/users', tags=['Users'])
# app.include_router(item.router, prefix='/items', tags=['Items'])

# Root endpoint for health check
@app.get("/", tags=["Health Check"])
async def root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the FastAPI project!"}

# Set up static files (if you have a 'static' directory)
# Create a 'static' directory in your project root if you need to serve static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    logger.warning("Static directory 'static' not found. Skipping static file mounting.")
    pass # Directory might not exist yet, so we pass

# Set up global error handling for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic validation errors, returning a structured JSON response.
    """
    logger.error(f"Validation Error: {exc.errors()} for request URL: {request.url}")
    error_details = []
    for error in exc.errors():
        error_details.append({
            "loc": [str(loc) for loc in error["loc"]], # Convert location tuple to list of strings
            "msg": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=422,
        content={"detail": error_details},
    )

# Generic exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handles any unhandled exceptions, returning a generic error response.
    """
    logger.exception(f"Unhandled Exception: {exc} for request URL: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# Set up server using Uvicorn
if __name__ == '__main__':
    logger.info("Starting Uvicorn server...")
    # You can load host and port from app.core.config.settings if needed
    uvicorn_config = Config(app=app, host='0.0.0.0', port=8000, log_level='info')
    server = Server(uvicorn_config)
    server.run()
