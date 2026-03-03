#!/usr/bin/env python3
"""
API Gateway Middleware with Rate Limiting

FastAPI middleware implementation for API Gateway with:
- Rate limiting
- API key authentication
- Request/response transformation

Usage:
    uvicorn api_gateway_middleware:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
from typing import Dict, Optional
import sys
from pathlib import Path

# Import rate limiting strategies
sys.path.insert(0, str(Path(__file__).parent))
from rate_limiting_strategies import RateLimiter, TokenBucketRateLimiter, SlidingWindowRateLimiter

app = FastAPI(
    title="API Gateway",
    description="API Gateway with rate limiting and authentication",
    version="1.0.0"
)

security = HTTPBearer()

# In-memory API key store (use database in production)
VALID_API_KEYS = {
    "valid-api-key-1": {"user_id": "user1", "tier": "premium"},
    "valid-api-key-2": {"user_id": "user2", "tier": "basic"},
}

# Rate limiters per tier
RATE_LIMITERS = {
    "premium": RateLimiter(max_requests=1000, window_seconds=60),
    "basic": RateLimiter(max_requests=100, window_seconds=60),
    "anonymous": RateLimiter(max_requests=10, window_seconds=60),
}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for rate limiting requests.

    Supports different rate limits based on:
    - API key tier (premium, basic)
    - IP address (for anonymous requests)
    """

    def __init__(self, app, limiters: Dict):
        super().__init__(app)
        self.limiters = limiters

    async def dispatch(self, request: Request, call_next):
        # Get client identifier
        client_id = request.client.host if request.client else "unknown"

        # Determine rate limiter based on authentication
        limiter = self.limiters.get("anonymous")
        tier = "anonymous"

        # Check for API key in header
        auth_header = request.headers.get("authorization")
        if auth_header:
            # Extract API key (Bearer token or direct)
            api_key = auth_header.replace("Bearer ", "").replace("bearer ", "")

            if api_key in VALID_API_KEYS:
                user_info = VALID_API_KEYS[api_key]
                tier = user_info.get("tier", "basic")
                limiter = self.limiters.get(tier, self.limiters["basic"])
                client_id = user_info.get("user_id", api_key)

        # Check rate limit
        if not limiter.is_allowed(client_id):
            remaining = limiter.get_remaining(client_id)
            reset_time = int(time.time()) + limiter.window_seconds

            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "retry_after": limiter.window_seconds
                },
                headers={
                    "X-RateLimit-Limit": str(limiter.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                    "Retry-After": str(limiter.window_seconds)
                }
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        remaining = limiter.get_remaining(client_id)
        reset_time = int(time.time()) + limiter.window_seconds

        response.headers["X-RateLimit-Limit"] = str(limiter.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)
        response.headers["X-RateLimit-Tier"] = tier

        return response


# Apply middleware
app.add_middleware(RateLimitMiddleware, limiters=RATE_LIMITERS)


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Verify API key and return user information.

    Args:
        credentials: HTTP Bearer token credentials

    Returns:
        User information dictionary

    Raises:
        HTTPException: If API key is invalid
    """
    api_key = credentials.credentials

    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return VALID_API_KEYS[api_key]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "API Gateway",
        "version": "1.0.0",
        "endpoints": {
            "data": "/api/v1/data",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint (no rate limiting)."""
    return {"status": "healthy"}


@app.get("/api/v1/data")
async def get_data(user_info: Dict = Depends(verify_api_key)):
    """
    Example API endpoint with authentication and rate limiting.

    Requires valid API key in Authorization header:
    Authorization: Bearer valid-api-key-1
    """
    return {
        "data": "example data",
        "user_id": user_info.get("user_id"),
        "tier": user_info.get("tier")
    }


@app.post("/api/v1/data")
async def create_data(
    request: Request,
    user_info: Dict = Depends(verify_api_key)
):
    """
    Example POST endpoint with authentication and rate limiting.
    """
    body = await request.json()
    return {
        "message": "Data created",
        "user_id": user_info.get("user_id"),
        "tier": user_info.get("tier"),
        "data": body
    }


@app.get("/api/v1/public")
async def public_endpoint(request: Request):
    """
    Public endpoint with rate limiting based on IP.

    No authentication required, but rate limited by IP address.
    """
    return {
        "message": "Public endpoint",
        "client_ip": request.client.host if request.client else "unknown"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
