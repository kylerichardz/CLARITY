import os
import logging
from dotenv import load_dotenv
from functools import lru_cache
from datetime import datetime
import json
import hashlib
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('clarity.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def load_env_variables() -> dict:
    """
    Load environment variables from .env file with caching
    
    Returns:
        Dict containing environment variables
    """
    logger.info("Loading environment variables")
    load_dotenv()
    
    required_vars = ['GOOGLE_API_KEY']
    env_vars = {}
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            logger.error(f"Missing required environment variable: {var}")
            raise ValueError(f"Missing required environment variable: {var}")
        env_vars[var] = value
    
    return env_vars 

def cache_response(cache_key: str, response: dict):
    """Cache response to disk"""
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    
    cache_file = cache_dir / f"{cache_key}.json"
    with open(cache_file, "w") as f:
        json.dump(response, f)

def get_cached_response(cache_key: str) -> dict:
    """Get cached response from disk"""
    cache_file = Path("cache") / f"{cache_key}.json"
    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)
    return None 