from app.config import settings
from app.utils.logger import get_logger
import time
from collections import defaultdict
from typing import Dict, Tuple
import asyncio

logger = get_logger(__name__)

class RateLimiter:
    def __init__(self):
        self.requests_per_minute = getattr(settings, 'RATE_LIMIT_REQUESTS', 60)
        self.period = getattr(settings, 'RATE_LIMIT_PERIOD', 60)
        self.requests: Dict[str, list] = defaultdict(list)
        self.total_requests = 0
        
    async def check_limit(self, client_id: str) -> Tuple[bool, Dict]:
        """
        Check if client has exceeded rate limit
        Returns: (is_allowed, limit_info)
        """
        now = time.time()
        window_start = now - self.period
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > window_start
        ]
        
        # Check limit
        current_count = len(self.requests[client_id])
        
        if current_count >= self.requests_per_minute:
            # Rate limited
            oldest = self.requests[client_id][0] if self.requests[client_id] else now
            reset_time = oldest + self.period
            
            limit_info = {
                "limit": self.requests_per_minute,
                "remaining": 0,
                "reset": reset_time,
                "retry_after": int(reset_time - now)
            }
            
            logger.warning(f"Rate limit exceeded for {client_id}")
            return False, limit_info
        
        # Add current request
        self.requests[client_id].append(now)
        self.total_requests += 1
        
        limit_info = {
            "limit": self.requests_per_minute,
            "remaining": self.requests_per_minute - current_count - 1,
            "reset": now + self.period
        }
        
        return True, limit_info
    
    def get_total_requests(self) -> int:
        """Get total requests processed"""
        return self.total_requests