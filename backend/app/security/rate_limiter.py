import time
from collections import defaultdict
from app.config import settings

class RateLimiter:
    """
    In-memory sliding window rate limiter.
    """
    def __init__(self, requests_per_minute: int = settings.RATE_LIMIT_PER_MINUTE):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        current_time = time.time()
        window_start = current_time - 60.0
        
        # Clean up old requests outside current 60s window
        self.requests[client_id] = [t for t in self.requests[client_id] if t > window_start]
        
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False
            
        self.requests[client_id].append(current_time)
        return True

rate_limiter = RateLimiter()

