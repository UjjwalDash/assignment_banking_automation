import time
from collections import defaultdict, deque
import threading

class SlidingWindowRateLimiter:
    def __init__(self, max_requests=5, window_size=1):
        """
        Initialize a sliding window rate limiter
        
        Args:
            max_requests (int): Maximum number of requests allowed in the window
            window_size (int): Size of the window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size  # in seconds
        # Using deque for efficient append/popleft operations
        self.request_timestamps = defaultdict(lambda: deque(maxlen=max_requests*2))
        self.lock = threading.Lock()
    
    def is_allowed(self, user_id):
        """
        Check if a request from the given user is allowed
        
        Args:
            user_id (str): Identifier for the user making the request
            
        Returns:
            bool: True if the request is allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()
            timestamps = self.request_timestamps[user_id]
            
            # Remove timestamps that are outside our window
            cutoff_time = current_time - self.window_size
            while timestamps and timestamps[0] < cutoff_time:
                timestamps.popleft()
            
            # Check if we're under the limit
            if len(timestamps) < self.max_requests:
                timestamps.append(current_time)
                return True
            
            return False
    
    def get_remaining_quota(self, user_id):
        """
        Get the number of remaining requests allowed for a user
        
        Args:
            user_id (str): Identifier for the user
            
        Returns:
            int: Number of remaining allowed requests in the current window
        """
        with self.lock:
            current_time = time.time()
            timestamps = self.request_timestamps[user_id]
            
            # Remove timestamps that are outside our window
            cutoff_time = current_time - self.window_size
            while timestamps and timestamps[0] < cutoff_time:
                timestamps.popleft()
            
            return max(0, self.max_requests - len(timestamps))
    
    def get_retry_after(self, user_id):
        """
        Get the time in seconds after which the user should retry
        
        Args:
            user_id (str): Identifier for the user
            
        Returns:
            float: Time in seconds to wait before the next request would be allowed
                  Returns 0 if requests are currently allowed
        """
        with self.lock:
            current_time = time.time()
            timestamps = self.request_timestamps[user_id]
            
            # If under the limit, no need to wait
            if len(timestamps) < self.max_requests:
                return 0
            
            # Calculate when the oldest request will expire from the window
            if timestamps:
                oldest_timestamp = timestamps[0]
                return max(0, (oldest_timestamp + self.window_size) - current_time)
            
            return 0

    def clear_user(self, user_id):
        """
        Clear all request history for a user
        
        Args:
            user_id (str): Identifier for the user
        """
        with self.lock:
            if user_id in self.request_timestamps:
                del self.request_timestamps[user_id]

# Standalone test
if __name__ == "__main__":
    # Create a rate limiter that allows 5 requests per second
    limiter = SlidingWindowRateLimiter(max_requests=5, window_size=1)
    user_id = "test_user"
    
    print("Testing Sliding Window Rate Limiter:")
    
    # Make 7 requests in quick succession
    for i in range(7):
        result = limiter.is_allowed(user_id)
        remaining = limiter.get_remaining_quota(user_id)
        print(f"Request {i+1}: {'Allowed' if result else 'Blocked'}, Remaining: {remaining}")
    
    if not result:
        retry_after = limiter.get_retry_after(user_id)
        print(f"Retry after: {retry_after:.2f} seconds")
        
        # Wait and try again
        print(f"Waiting {retry_after:.2f} seconds...")
        time.sleep(retry_after)
        result = limiter.is_allowed(user_id)
        print(f"After waiting - Request allowed: {result}")