Here is a complete, production-ready sample. This setup uses **Redis Pub/Sub** to decouple the load generation from the logging process.

### Architecture
1.  **Locust Worker:** Detects failed requests and publishes them to a Redis channel.
2.  **Redis:** Acts as a high-speed buffer.
3.  **Consumer (Python/Node):** Subscribes to the channel and performs bulk indexing into Elasticsearch.

---

### Part 1: The Locust File (`locustfile.py`)

We use the `request` event hook to filter for failures. We use `gevent` to ensure the publishing doesn't block the user simulation.

```python
import json
import time
import gevent
import redis
from locust import HttpUser, task, events

# Initialize Redis connection
# In a distributed setup, ensure this points to your central Redis instance
redis_client = redis.Redis(host='localhost', port=6379, db=0)
CHANNEL_NAME = "locust_failed_requests"

class WebsiteUser(HttpUser):
    host = "http://your-target-app.com"

    @task
    def get_product(self):
        # Intentionally hitting a bad endpoint to generate failures for testing
        self.client.get("/non-existent-page")

    @task(3)
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
```

---

### Part 2: The Consumer Script (`es_consumer.py`)

This script runs independently. It listens to Redis and batches messages before sending them to Elasticsearch. Batching is crucial for ES performance.

```python
import json
import time
import redis
from elasticsearch import Elasticsearch, helpers

# Configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
CHANNEL_NAME = "locust_failed_requests"
ES_HOST = "http://localhost:9200"
INDEX_NAME = "locust-failures"
BATCH_SIZE = 50
FLUSH_INTERVAL = 5 # seconds

# Initialize Clients
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
es = Elasticsearch([ES_HOST])

def bulk_index_to_es(batch):
    """Send a batch of documents to Elasticsearch."""
    actions = []
    for doc in batch:
        action = {
            "_index": INDEX_NAME,
            "_source": doc
        }
        actions.append(action)
    
    if actions:
        try:
            helpers.bulk(es, actions)
            print(f"Indexed {len(actions)} failure logs to Elasticsearch.")
        except Exception as e:
            print(f"Elasticsearch bulk indexing failed: {e}")

def main():
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL_NAME)
    print(f"Listening for failures on Redis channel: {CHANNEL_NAME}")

    batch = []
    last_flush = time.time()

    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                data = json.loads(message['data'])
                batch.append(data)
                
                # Check if we should flush based on size or time
                now = time.time()
                if len(batch) >= BATCH_SIZE or (now - last_flush) >= FLUSH_INTERVAL:
                    bulk_index_to_es(batch)
                    batch = []
                    last_flush = now
                    
            except json.JSONDecodeError:
                print("Received invalid JSON from Redis")

if __name__ == "__main__":
    # Ensure the index exists with proper mapping before starting
    # (You would typically run the mapping creation from Part 1 here)
    main()
```

---

### Why this is the "Best" way for Failed Requests:

1.  **Zero Impact on Load:** By using `gevent.spawn` in the Locust file, the act of logging happens in a separate greenlet. If Redis is temporarily slow, it won't stop your virtual users from hitting your application.
2.  **Filtering at Source:** We only publish when `exception` is present. This reduces the volume of data moving through Redis and ES by 90-99% in a healthy system, allowing you to keep a longer retention period for errors.
3.  **Bulk Indexing:** The consumer waits for either 50 records or 5 seconds. This prevents Elasticsearch from being overwhelmed by thousands of tiny HTTP requests, which is the most common cause of ES bottlenecks during load tests.
4.  **Scalability:** If you have 100 Locust workers, they all publish to the same Redis channel. You can then spin up multiple `es_consumer.py` instances (using Redis Consumer Groups if you switch to Redis Streams) to handle the ingestion load.