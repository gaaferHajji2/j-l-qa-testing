import os
import json
import time
import gevent
import redis
from locust import HttpUser, task, events
from dotenv import load_dotenv

load_dotenv()

# Initialize Redis connection
# In a distributed setup, ensure this points to your central Redis instance
redis_client = redis.Redis(
    host=os.getenv('redis_host', ''), 
    port=int(os.getenv('redis_port', 0)), 
    db=int(os.getenv('redis_db', -1))
)
CHANNEL_NAME = os.getenv('channel_name')

class WebsiteUser(HttpUser):
    @task
    def get_product(self):
        # Intentionally hitting a bad endpoint to generate failures for testing
        self.client.get("/non-existent-page")

    @task(5)
    def get_home(self):
        self.client.get("/")

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """Ensure we don't run this logic on the master node in distributed mode."""
    if environment.runner is not None:
        print(f"Locust worker initialized. Publishing failures to Redis channel: {CHANNEL_NAME}")

@events.request.add_listener
def handle_request_failure(request_type, name, response_time, response_length, exception, context, **kwargs):
    """
    Only capture requests that resulted in an exception or non-2xx status.
    """
    if exception:
        log_data = {
            "timestamp": time.time(),
            "test_name": "my-load-test",
            "request_type": request_type,
            "name": name,
            "response_time": response_time,
            "exception": str(exception),
            "context": context
        }
        
        # Use gevent to send to Redis asynchronously so it doesn't block the user
        gevent.spawn(publish_to_redis, json.dumps(log_data))

def publish_to_redis(message):
    try:
        redis_client.publish(CHANNEL_NAME, message)
    except Exception as e:
        print(f"Failed to publish to Redis: {e}")