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

class AdminLoginRateLimiter:
    """
    Sliding window rate limiter for administrative login endpoint.
    Restricts login attempts to 5 attempts per 15 minutes (900 seconds) per IP.
    """
    def __init__(self, max_attempts: int = 5, window_seconds: int = 900):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.attempts = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        current_time = time.time()
        window_start = current_time - self.window_seconds
        # Clean up timestamps older than the 15-minute sliding window
        self.attempts[client_id] = [t for t in self.attempts[client_id] if t > window_start]
        if len(self.attempts[client_id]) >= self.max_attempts:
            return False
        self.attempts[client_id].append(current_time)
        return True

admin_login_rate_limiter = AdminLoginRateLimiter(max_attempts=5, window_seconds=900)

