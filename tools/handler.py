""" API Handler"""
from typing import Dict, Any, Optional
import logging
from functools import wraps
import json
import time
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom exception for API-related errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

def api_handler(
    max_retries: int = 0,
    retry_delay: float = 1.0,
    timeout: int = 30
):
    """
    Decorator for handling API requests with error handling and retries.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        retry_delay (float): Delay between retries in seconds
        timeout (int): Request timeout in seconds
    
    Example usage:
    
    @api_handler(max_retries=3, retry_delay=1.0)
    def get_user_data(user_id: str) -> Dict:
        response = requests.get(
            f"https://api.example.com/users/{user_id}",
            headers={"Authorization": "Bearer your-token"}
        )
        return response
    
    @api_handler()
    def create_post(data: Dict) -> Dict:
        response = requests.post(
            "https://api.example.com/posts",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        return response
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Always try at least once, even if max_retries is 0
            for attempt in range(max_retries + 1):
                try:
                    response = func(*args, **kwargs)
                    # Ensure we have a requests.Response object
                    if not isinstance(response, requests.Response):
                        return response
                    
                    # Log the raw response for debugging
                    logger.info(f"Raw response: {response.text[:1000]}")  # First 1000 chars
                    logger.info(f"Response status code: {response.status_code}")
                    logger.info(f"Response headers: {response.headers}")
                    
                    response.raise_for_status()         
                    try:
                        return response.json()
                    except json.JSONDecodeError as json_err:
                        logger.error(f"JSON decode error: {str(json_err)}")
                        logger.error(f"Response content: {response.text[:1000]}")  # First 1000 chars
                        raise APIError(f"Invalid JSON response: {str(json_err)}", 
                                     status_code=response.status_code,
                                     response=response.text)
                
                except requests.exceptions.RequestException as e:
                    error_msg = f"Request failed: {str(e)}"
                    status_code = getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
                    response_text = getattr(e.response, 'text', None) if hasattr(e, 'response') else None
                    
                    logger.error(f"Request error: {error_msg}")
                    if response_text:
                        logger.error(f"Response content: {response_text[:1000]}")
                    
                    if attempt == max_retries:
                        logger.error(f"Final attempt failed: {error_msg}")
                        raise APIError(error_msg, status_code=status_code, response=response_text)
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {error_msg}. Retrying...")
                    
                    # Add progress logging for longer delays
                    total_delay = retry_delay * (attempt + 1)  # Exponential backoff
                    if total_delay > 5:
                        logger.info(f"Retrying in {total_delay:.1f} seconds...")
                        remaining_delay = total_delay
                        while remaining_delay > 0:
                            time.sleep(min(5, remaining_delay))
                            remaining_delay -= 5
                            if remaining_delay > 0:
                                logger.info(f"{remaining_delay:.1f} seconds remaining until retry...")
                    else:
                        time.sleep(total_delay)
                    
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}")
                    raise APIError(f"Unexpected error: {str(e)}")
            
            return None
        return wrapper
    return decorator
