from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.exceptions import AppException
from app.utils.logger import get_logger
import traceback
from typing import Union
from app.config import settings

logger = get_logger(__name__)

def setup_error_handlers(app: FastAPI):
    """Setup global error handlers"""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Handle custom application exceptions"""
        logger.error(
            f"App exception: {exc.message}",
            extra={
                "status_code": exc.status_code,
                "details": exc.details,
                "path": request.url.path
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.__class__.__name__,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, 
        exc: RequestValidationError
    ):
        """Handle request validation errors"""
        errors = []
        for error in exc.errors():
            errors.append({
                "loc": " -> ".join(str(x) for x in error["loc"]),
                "msg": error["msg"],
                "type": error["type"]
            })
        
        logger.warning(
            f"Validation error: {errors}",
            extra={"path": request.url.path}
        )
        
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": {"errors": errors}
                }
            }
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, 
        exc: StarletteHTTPException
    ):
        """Handle HTTP exceptions"""
        logger.error(
            f"HTTP exception: {exc.detail}",
            extra={
                "status_code": exc.status_code,
                "path": request.url.path
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": exc.detail
                }
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all unhandled exceptions"""
        # Log full traceback in development
        if settings.DEBUG:
            error_detail = {
                "message": str(exc),
                "traceback": traceback.format_exc().split("\n")
            }
        else:
            error_detail = {"message": "Internal server error"}
        
        logger.error(
            f"Unhandled exception: {str(exc)}",
            extra={
                "path": request.url.path,
                "traceback": traceback.format_exc() if settings.DEBUG else None
            }
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "details": error_detail if settings.DEBUG else None
                }
            }
        )