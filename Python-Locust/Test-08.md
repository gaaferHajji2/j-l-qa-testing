Using JSON-formatted logs in Locust is highly recommended, especially for distributed testing. JSON logs are machine-readable, making it easy to ingest them into centralized logging systems like **ELK (Elasticsearch, Logstash, Kibana)**, **Loki**, or **CloudWatch**.

Here is how to set it up effectively.

### 1. The Setup: `python-json-logger`
The standard library `logging` module doesn't output JSON by default. The most common and robust way to achieve this is using the `python-json-logger` package.

**Install the package:**
```bash
pip install python-json-logger
```

### 2. Basic Implementation in `locustfile.py`

You need to configure the root logger or a specific logger to use the `JsonFormatter`.

```python
import logging
from pythonjsonlogger.jsonlogger import JsonFormatter
from locust import HttpUser, task, between

# 1. Configure the Logger
logger = logging.getLogger("locust_user")
logger.setLevel(logging.INFO)

# 2. Create a Console Handler
console_handler = logging.StreamHandler()

# 3. Define the JSON Format
# You can customize which fields appear in the JSON
log_format = "%(asctime)s %(levelname)s %(name)s %(message)s"
formatter = JsonFormatter(log_format)

# 4. Attach Formatter to Handler
console_handler.setFormatter(formatter)

# 5. Attach Handler to Logger
logger.addHandler(console_handler)

class JsonLogUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def home_page(self):
        # Standard info log
        logger.info("Starting home page request")
        
        try:
            response = self.client.get("/")
            if response.status_code == 200:
                # Log with extra context (automatically added to JSON)
                logger.info("Request successful", extra={
                    "status_code": response.status_code,
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                })
            else:
                logger.warning("Request failed", extra={
                    "status_code": response.status_code,
                    "url": response.url
                })
        except Exception as e:
            logger.error("Request exception", extra={
                "error": str(e)
            })
```

### 3. Output Example
When you run this, instead of plain text, you will see structured JSON lines in your terminal:

```json
{
  "asctime": "2026-07-06 10:00:01,123",
  "levelname": "INFO",
  "name": "locust_user",
  "message": "Starting home page request"
}
{
  "asctime": "2026-07-06 10:00:01,456",
  "levelname": "INFO",
  "name": "locust_user",
  "message": "Request successful",
  "status_code": 200,
  "response_time_ms": 120.5
}
```

### 4. Advanced: Adding Context Automatically
In distributed testing, it's crucial to know **which worker** and **which user** generated the log. You can create a custom filter to inject this context into every log record automatically.

```python
import logging
import json
from pythonjsonlogger.jsonlogger import JsonFormatter
from locust import HttpUser, task, events

class ContextFilter(logging.Filter):
    """Adds Locust context to every log record"""
    def filter(self, record):
        # Try to get runner info if available
        try:
            # 'environment' might not be available during initial import
            if hasattr(record, 'msg') and isinstance(record.msg, dict):
                pass # Already handled by extra={}
            
            # Note: Accessing self.environment inside a filter is tricky 
            # because filters are static. It's often better to pass 
            # context via 'extra' in the task itself.
        except:
            pass
        return True

# Configure Logger
logger = logging.getLogger("locust_json")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = JsonFormatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class SmartUser(HttpUser):
    @task
    def my_task(self):
        # Manually inject context for this specific user instance
        logger.info("Action started", extra={
            "worker_id": self.environment.runner.client_id if self.environment.runner else "unknown",
            "user_class": self.__class__.__name__
        })
        self.client.get("/")
```

### 5. Using JSON Logs with Docker Compose
When running in Docker, JSON logs are powerful because you can pipe `stdout` directly to a log aggregator.

**`docker-compose.yml`**
```yaml
version: '3'
services:
  worker:
    image: locustio/locust
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/locustfile.py --worker --master-host master
    # Docker captures stdout, which now contains JSON
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 6. Best Practices for JSON Logging in Locust

1. **Use `extra` for Dynamic Data:** Don't format strings into the message (e.g., `f"User {id} logged in"`). Instead, use `logger.info("User logged in", extra={"user_id": id})`. This allows your logging backend (like Elasticsearch) to index `user_id` as a searchable field.
2. **Avoid Logging Sensitive Data:** Ensure that tokens, passwords, or PII are never passed into the `extra` dictionary.
3. **Handle Exceptions Properly:** Use `logger.exception()` inside `except` blocks. It automatically includes the stack trace in the JSON output under a `exc_info` or `stack_trace` field (depending on the formatter configuration).
4. **Performance Impact:** JSON formatting is slightly slower than plain text. For extremely high-RPS tests (10k+ RPS per worker), consider sampling your logs (e.g., only log every 100th request) or logging only errors/warnings.

### Summary
By using `python-json-logger` and the `extra` parameter, you transform your Locust logs from simple text lines into rich, structured data events. This is the foundation for effective observability in distributed performance testing.