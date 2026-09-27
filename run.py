#!/usr/bin/env python3
"""Run FitBuddy FastAPI application."""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION} on http://127.0.0.1:{settings.PORT}")
    print(f"Interactive API Docs available at http://127.0.0.1:{settings.PORT}/docs")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
