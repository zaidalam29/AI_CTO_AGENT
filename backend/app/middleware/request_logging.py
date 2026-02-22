from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import get_logger
import time

logger = get_logger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get request ID from state if set by previous middleware
        request_id = getattr(request.state, "request_id", None)
        
        # Log request
        logger.info(
            f"Request started: {request.method} {request.url.path}"
        )
        
        # Process request
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response - FIXED: without extra parameter
            logger.info(
                f"Request completed: {request.method} {request.url.path} - {response.status_code} ({process_time*1000:.2f}ms)"
            )
            
            # Add processing time header
            response.headers["X-Process-Time"] = str(process_time)
            if request_id:
                response.headers["X-Request-ID"] = request_id
                
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path} - {str(e)}"
            )
            raise