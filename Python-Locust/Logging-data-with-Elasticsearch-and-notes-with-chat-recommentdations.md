In a distributed mode (Master/Worker setup), logging is tricky because your test load is spread across multiple machines. If you just use standard Python `print()` or basic file logging, your logs will be scattered across different servers and lost when the workers shut down.

The "best" way depends on how much infrastructure you want to manage. Here are the three most effective approaches, ranked from **Professional/Scalable** to **Simple/Lightweight**.

### 1. The Professional Way: Elasticsearch + Locust Event Listeners
You mentioned this, and it is indeed the industry standard for large-scale performance testing. It allows you to correlate performance metrics with specific error logs in real-time.

**How it works:**
You use Locust's built-in `request_failure` event hook. Every time a request fails (whether due to status code or your custom time assertion), you send that data to Elasticsearch.

**Why it's great for Distributed Mode:**
*   **Centralization:** All workers send logs to one central ES cluster.
*   **Context:** You can log the `tenant_id`, `response_time`, and `exception` together.
*   **Visualization:** You can build Kibana dashboards to see "Which tenants are causing the most timeouts?"

**Implementation Example:**

```python
import json
from locust import events
from elasticsearch import Elasticsearch

# Initialize ES client (do this once at the module level)
es = Elasticsearch(["http://your-es-host:9200"])

@events.request_failure.add_listener
def log_failure_to_es(request_type, name, response_time, exception, context, **kwargs):
    """
    This listener runs on EVERY worker node whenever a failure occurs.
    """
    log_entry = {
        "@timestamp": datetime.now().isoformat(),
        "test_run_id": context.get("test_run_id", "unknown"), # Pass this via environment
        "tenant_id": context.get("tenant_id", "unknown"),     # From your multitenant user
        "request_type": request_type,
        "endpoint": name,
        "response_time_ms": response_time,
        "error_message": str(exception),
        "worker_hostname": socket.gethostname() # Useful to identify which worker failed
    }
    
    try:
        es.index(index="locust-logs", document=log_entry)
    except Exception as e:
        print(f"Failed to send log to ES: {e}")
```

---

### 2. The Lightweight Way: Centralized JSON File (via Master Node)
If setting up Elasticsearch feels like overkill, you can use Locust's **Master-Worker communication** features. Workers can send messages to the Master, and the Master can write them to a single file.

**How it works:**
1.  Workers catch the error.
2.  Workers send a message to the Master using `environment.runner.send_message()`.
3.  The Master receives the message and appends it to a `failures.json` file.

**Implementation Example:**

**On the Worker (in your tasks):**
```python
from locust import events

@events.request_failure.add_listener
def report_failure_to_master(request_type, name, response_time, exception, context, **kwargs):
    if environment.runner is not None and hasattr(environment.runner, 'send_message'):
        environment.runner.send_message("log_failure", {
            "time": response_time,
            "error": str(exception),
            "tenant": context.get("tenant_id")
        })
```

**On the Master (in a separate `master_logger.py` file):**
```python
import json
from locust import events

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        @environment.runner.message_listener("log_failure")
        def handle_failure_log(msg, **kwargs):
            with open("central_failures.json", "a") as f:
                f.write(json.dumps(msg.data) + "\n")
```

---

### 3. The "Quick & Dirty" Way: Locust's Built-in CSV/HTML Reports
If you don't need detailed error *messages* but just want to know *that* they happened, Locust already does this for you.

*   **CSV Output:** When you run with `--csv=reports/my_test`, Locust generates a `_failures.csv` file.
*   **Limitation:** In distributed mode, these files are only generated on the **Master** node. They will tell you the count of failures and the average response time of those failures, but they won't give you the specific stack trace or the `tenant_id` that caused it.

---

### Comparison Table

| Feature | Elasticsearch (Event Listener) | Master-Worker Messaging | Built-in CSV |
| :--- | :--- | :--- | :--- |
| **Setup Difficulty** | High (Need ES/Kibana) | Medium (Custom Python logic) | Low (Zero config) |
| **Data Detail** | Very High (Full context) | High (Customizable) | Low (Aggregated stats) |
| **Real-time?** | Yes | Yes (during test) | No (Post-test) |
| **Best For** | Enterprise/Complex Apps | Mid-sized teams | Quick smoke tests |

### Recommendation for Your Multitenant App:
Since you are building a complex **Multitenant** application with many sub-apps, I strongly recommend **Option 1 (Elasticsearch)**. 

**Why?** 
When a request takes > 5 seconds, you need to know:
1.  Which **Tenant** was it? (Is one tenant hogging resources?)
2.  Which **Sub-app** was it? (POD vs Sales?)
3.  Which **Worker** handled it? (Is one load generator machine having network issues?)

Only Elasticsearch (or a similar tool like Grafana Loki) will allow you to slice and dice this data effectively after the test is finished.