import redis
import json

# Connects to the Redis container
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_latest_price(ticker: str, data: dict):
    """Caches the absolute latest state for quick agent retrieval."""
    redis_client.set(f"latest_market:{ticker}", json.dumps(data))

def get_cached_price(ticker: str):
    data = redis_client.get(f"latest_market:{ticker}")
    return json.loads(data) if data else None