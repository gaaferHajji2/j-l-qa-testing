To log data from Locust workers to a specific file in JSON format, you need to configure Python's `logging` module to use a `FileHandler` combined with a JSON formatter.

Here is the step-by-step implementation:

### 1. Prerequisites
You will need the `python-json-logger` package to handle the formatting easily.
```bash
pip install python-json-logger
```

### 2. Implementation in `locustfile.py`

```python
import logging
from pythonjsonlogger.jsonlogger import JsonFormatter
from locust import HttpUser, task, between

# 1. Create a logger instance
logger = logging.getLogger("locust_worker_logger")
logger.setLevel(logging.INFO)

# 2. Create a File Handler pointing to your specific file
# 'a' mode appends to the file so logs aren't lost if multiple workers write to it
file_handler = logging.FileHandler("worker_logs.json", mode='a')

# 3. Define the JSON format
# You can include any standard logging attributes here
log_format = "%(asctime)s %(levelname)s %(name)s %(message)s"
formatter = JsonFormatter(log_format)

# 4. Attach the formatter to the handler and the handler to the logger
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class JsonFileUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def log_to_file(self):
        response = self.client.get("/")
        
        # Log basic info
        logger.info("Request completed", extra={
            "status_code": response.status_code,
            "url": response.url,
            "response_time_ms": response.elapsed.total_seconds() * 1000
        })

        if response.status_code != 200:
            logger.warning("Non-200 status received", extra={
                "status_code": response.status_code
            })
```

### 3. Handling Distributed Workers (Important)
If you are running multiple workers via Docker Compose, having them all write to the **same** file on the host machine can cause "file locking" issues or corrupted JSON lines.

**Option A: Unique Files per Worker (Recommended for simplicity)**
Use an environment variable to give each worker its own log file.

In your `docker-compose.yml`:
```yaml
services:
  worker:
    image: locustio/locust
    volumes:
      - ./logs:/mnt/logs # Mount a folder to store logs
    environment:
      - LOG_FILE_PATH=/mnt/logs/worker_${HOSTNAME}.json
    command: -f /mnt/locust/locustfile.py --worker --master-host master
```

In your `locustfile.py`:
```python
import os
import logging
from pythonjsonlogger.jsonlogger import JsonFormatter

logger = logging.getLogger("locust_worker")
logger.setLevel(logging.INFO)

# Get path from environment variable or default
log_path = os.getenv("LOG_FILE_PATH", "worker_default.json")
file_handler = logging.FileHandler(log_path, mode='a')

formatter = JsonFormatter("%(asctime)s %(levelname)s %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
```

**Option B: Centralized Logging (Better for analysis)**
Instead of writing to local files, send the JSON logs directly to a centralized service like Elasticsearch or Loki using an HTTP handler (as discussed in the previous section). This avoids file management entirely.

### 4. What the Output Looks Like
Your `worker_logs.json` file will contain one JSON object per line:

```json
{"asctime": "2026-07-06 14:30:01,123", "levelname": "INFO", "name": "locust_worker_logger", "message": "Request completed", "status_code": 200, "url": "http://example.com/", "response_time_ms": 45.2}
{"asctime": "2026-07-06 14:30:02,456", "levelname": "WARNING", "name": "locust_worker_logger", "message": "Non-200 status received", "status_code": 500}
```

### Key Tips for File Logging in Locust:
1.  **Use `mode='a'`**: Always append to the file. If you use `'w'`, every time a new user starts or the script reloads, it might wipe the previous logs.
2.  **Performance**: Writing to disk is slower than writing to memory. For very high-load tests, consider logging only errors (`logger.setLevel(logging.ERROR)`) or using a centralized HTTP-based logger to keep the workers fast.
3.  **Rotation**: If the test runs for a long time, the file can get huge. You can use `logging.handlers.RotatingFileHandler` instead of `FileHandler` to automatically create new files when the size limit is reached.