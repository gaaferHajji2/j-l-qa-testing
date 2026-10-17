To add custom variables (like `tenant_id`, `route_name`, or `module`) to the context in a failure event, you need to understand that Locust's `context` is a **dictionary** attached to the specific request.

There are two ways to do this: **Implicitly** (via the User object) and **Explicitly** (via the Request call).

### Method 1: The "User Attribute" Way (Recommended for Multitenancy)
Since you have a `MultitenantUser` base class, the cleanest way is to store your custom variables as attributes of the `self.user` object. Locust automatically passes the user instance into the `context` of the event listener.

**1. In your Task/Script:**
Set the variable on `self.user` before making the request.

```python
from locust import task, TaskSet

class RouteTasks(TaskSet):
    @task
    def create_route(self):
        # Set custom context variables on the user instance
        self.user.tenant_id = "tenant_123" 
        self.user.module_name = "POD_Routes"
        
        payload = {"name": "Route A"}
        
        with self.client.post("/api/v1/routes", json=payload, catch_response=True) as response:
            if response.status_code != 201:
                # Trigger a manual failure
                response.failure("Status code was not 201")
```

**2. In your Event Listener (Master or Worker):**
Access these variables through `context["user"]`.

```python
from locust import events

@events.request_failure.add_listener
def log_custom_context(request_type, name, response_time, exception, context, **kwargs):
    # Extract the user instance from the context
    user = context.get("user")
    
    if user:
        tenant_id = getattr(user, 'tenant_id', 'Unknown')
        module = getattr(user, 'module_name', 'Unknown')
        
        print(f"FAILURE in {module} for Tenant {tenant_id}: {exception}")
        
        # If sending to Master:
        if environment.runner:
            environment.runner.send_message("log_failure", {
                "tenant_id": tenant_id,
                "module": module,
                "error": str(exception),
                "time": response_time
            })
```

---

### Method 2: The "Explicit Context" Way (Per-Request)
If you don't want to clutter your User object, or if the variable changes for every single request (like a specific `consignment_id`), you can pass a `context` dictionary directly into the HTTP request method.

**1. In your Task/Script:**
Pass the `context` argument to `self.client.get/post`.

```python
@task
def get_consignment(self):
    consignment_id = "CONS-999"
    
    # Pass custom data directly into the request's context
    custom_ctx = {
        "consignment_id": consignment_id,
        "test_phase": "load_test_1"
    }

    with self.client.get(f"/api/v1/consignments/{consignment_id}", 
                         context=custom_ctx, 
                         catch_response=True) as response:
        if response.time > 5000:
            response.failure("Too slow")
```

**2. In your Event Listener:**
The `context` parameter in the listener will now contain your custom keys.

```python
@events.request_failure.add_listener
def log_explicit_context(request_type, name, response_time, exception, context, **kwargs):
    # Access the custom dictionary you passed in the request
    consignment_id = context.get("consignment_id", "N/A")
    test_phase = context.get("test_phase", "N/A")
    
    print(f"Failed Consignment: {consignment_id} during phase: {test_phase}")
```

---

### How to Send This to the Master Node

When using **Distributed Mode**, the `request_failure` event fires on the **Worker**. To get this data to the Master, you combine the logic above with the `send_message` function.

**Complete Example (Worker Side):**

```python
import socket
from locust import events, task
from locust.runners import WorkerRunner

# Global reference to environment (set in on_start or init)
environment = None 

@events.init.add_listener
def on_locust_init(env, **_kwargs):
    global environment
    environment = env

@events.request_failure.add_listener
def handle_failure_and_notify_master(request_type, name, response_time, exception, context, **kwargs):
    # Only run this logic if we are a Worker
    if isinstance(environment.runner, WorkerRunner):
        
        # 1. Gather Custom Data
        user = context.get("user")
        tenant_id = getattr(user, 'tenant_id', 'Unknown') if user else 'Unknown'
        
        # 2. Prepare Payload
        payload = {
            "worker_hostname": socket.gethostname(),
            "tenant_id": tenant_id,
            "endpoint": name,
            "response_time_ms": response_time,
            "error_details": str(exception)
        }
        
        # 3. Send to Master
        environment.runner.send_message("custom_failure_log", payload)
```

**Complete Example (Master Side):**

```python
from locust import events
from locust.runners import MasterRunner
import json

@events.init.add_listener
def on_locust_init(env, **_kwargs):
    if isinstance(env.runner, MasterRunner):
        # Register a listener for our custom message
        @env.runner.message_listener("custom_failure_log")
        def receive_failure_log(msg, **kwargs):
            data = msg.data
            # Now you can log this to Elasticsearch, a file, or a DB
            print(f"[MASTER LOG] Tenant {data['tenant_id']} failed on {data['endpoint']}: {data['error_details']}")
            
            # Example: Write to a central JSONL file
            with open("master_failures.jsonl", "a") as f:
                f.write(json.dumps(data) + "\n")
```

### Summary of Best Practice
*   Use **Method 1 (User Attributes)** for things that stay the same for the whole user session (like `tenant_id`).
*   Use **Method 2 (Explicit Context)** for things that change per request (like `item_id` or `batch_number`).
*   Always check `isinstance(environment.runner, WorkerRunner)` before sending messages to avoid errors when running in standalone mode.