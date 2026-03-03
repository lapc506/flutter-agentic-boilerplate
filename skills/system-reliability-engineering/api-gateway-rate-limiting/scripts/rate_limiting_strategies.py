#!/usr/bin/env python3
"""
Rate Limiting Strategies

Implementation of different rate limiting algorithms:
- Fixed Window
- Sliding Window
- Token Bucket

Usage:
    # As a library
    from rate_limiting_strategies import RateLimiter, TokenBucketRateLimiter

    limiter = RateLimiter(max_requests=100, window_seconds=60)
    if limiter.is_allowed("user123"):
        # Process request
        pass

    # CLI testing
    python rate_limiting_strategies.py --strategy fixed --max-requests 10 --window 60
"""

import argparse
import time
from typing import Dict, Optional
from collections import defaultdict, deque


class RateLimiter:
    """
    Fixed Window Rate Limiter.

    Simple rate limiting that resets at fixed intervals.
    Good for: Simple use cases, predictable traffic
    """

    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize fixed window rate limiter.

        Args:
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed.

        Args:
            identifier: Unique identifier (IP, user ID, API key, etc.)

        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        user_requests = self.requests[identifier]

        # Remove old requests outside window
        while user_requests and user_requests[0] < now - self.window_seconds:
            user_requests.popleft()

        # Check if limit exceeded
        if len(user_requests) >= self.max_requests:
            return False

        # Add current request
        user_requests.append(now)
        return True

    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests in current window."""
        now = time.time()
        user_requests = self.requests[identifier]

        # Remove old requests
        while user_requests and user_requests[0] < now - self.window_seconds:
            user_requests.popleft()

        return max(0, self.max_requests - len(user_requests))

    def reset(self, identifier: Optional[str] = None):
        """Reset rate limit for identifier or all."""
        if identifier:
            self.requests[identifier].clear()
        else:
            self.requests.clear()


class TokenBucketRateLimiter:
    """
    Token Bucket Rate Limiter.

    Allows bursts up to capacity, then refills at constant rate.
    Good for: Burst traffic, smooth rate limiting
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = defaultdict(lambda: capacity)
        self.last_refill = defaultdict(time.time)

    def is_allowed(self, identifier: str, tokens: int = 1) -> bool:
        """
        Check if request is allowed (consumes tokens).

        Args:
            identifier: Unique identifier
            tokens: Number of tokens to consume (default: 1)

        Returns:
            True if enough tokens available, False otherwise
        """
        now = time.time()
        last = self.last_refill[identifier]

        # Refill tokens based on elapsed time
        elapsed = now - last
        refill_amount = elapsed * self.refill_rate
        self.tokens[identifier] = min(
            self.capacity,
            self.tokens[identifier] + refill_amount
        )
        self.last_refill[identifier] = now

        # Check if enough tokens
        if self.tokens[identifier] >= tokens:
            self.tokens[identifier] -= tokens
            return True

        return False

    def get_remaining(self, identifier: str) -> float:
        """Get remaining tokens."""
        now = time.time()
        last = self.last_refill[identifier]

        # Refill tokens
        elapsed = now - last
        refill_amount = elapsed * self.refill_rate
        current_tokens = min(
            self.capacity,
            self.tokens[identifier] + refill_amount
        )
        self.last_refill[identifier] = now

        return current_tokens


class SlidingWindowRateLimiter:
    """
    Sliding Window Rate Limiter.

    Tracks requests in a sliding time window.
    Good for: Accurate rate limiting, no burst at window boundaries
    """

    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize sliding window rate limiter.

        Args:
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.windows = defaultdict(deque)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed.

        Args:
            identifier: Unique identifier

        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        window_start = now - self.window_seconds

        # Get user's request timestamps
        user_windows = self.windows[identifier]

        # Remove old requests outside window
        while user_windows and user_windows[0] < window_start:
            user_windows.popleft()

        # Check limit
        if len(user_windows) >= self.max_requests:
            return False

        # Add current request
        user_windows.append(now)
        return True

    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests in current window."""
        now = time.time()
        window_start = now - self.window_seconds
        user_windows = self.windows[identifier]

        # Remove old requests
        while user_windows and user_windows[0] < window_start:
            user_windows.popleft()

        return max(0, self.max_requests - len(user_windows))


def test_limiter(limiter, identifier: str = "test", num_requests: int = 15):
    """Test rate limiter with multiple requests."""
    print(f"\nTesting {limiter.__class__.__name__}")
    print(f"Identifier: {identifier}")
    print(f"Attempting {num_requests} requests...\n")

    allowed = 0
    denied = 0

    for i in range(num_requests):
        if limiter.is_allowed(identifier):
            allowed += 1
            remaining = limiter.get_remaining(identifier)
            print(f"Request {i+1}: ✅ Allowed (remaining: {remaining})")
        else:
            denied += 1
            remaining = limiter.get_remaining(identifier)
            print(f"Request {i+1}: ❌ Denied (remaining: {remaining})")

        time.sleep(0.1)  # Small delay between requests

    print(f"\nResults: {allowed} allowed, {denied} denied")


def main():
    """CLI entry point for testing rate limiters."""
    parser = argparse.ArgumentParser(
        description="Test rate limiting strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--strategy",
        choices=["fixed", "token-bucket", "sliding"],
        default="fixed",
        help="Rate limiting strategy"
    )

    parser.add_argument(
        "--max-requests",
        type=int,
        default=10,
        help="Maximum requests allowed"
    )

    parser.add_argument(
        "--window",
        type=int,
        default=60,
        help="Time window in seconds (for fixed/sliding)"
    )

    parser.add_argument(
        "--capacity",
        type=int,
        default=10,
        help="Token bucket capacity"
    )

    parser.add_argument(
        "--refill-rate",
        type=float,
        default=1.0,
        help="Token bucket refill rate (tokens/second)"
    )

    parser.add_argument(
        "--num-requests",
        type=int,
        default=15,
        help="Number of requests to test"
    )

    parser.add_argument(
        "--identifier",
        default="test-user",
        help="Identifier for rate limiting"
    )

    args = parser.parse_args()

    # Create appropriate limiter
    if args.strategy == "fixed":
        limiter = RateLimiter(args.max_requests, args.window)
    elif args.strategy == "token-bucket":
        limiter = TokenBucketRateLimiter(args.capacity, args.refill_rate)
    elif args.strategy == "sliding":
        limiter = SlidingWindowRateLimiter(args.max_requests, args.window)

    # Run test
    test_limiter(limiter, args.identifier, args.num_requests)

    return 0


if __name__ == "__main__":
    exit(main())
