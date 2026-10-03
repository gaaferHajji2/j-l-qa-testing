Here is a complete Locust performance test suite tailored specifically for the `ws` Node.js server created previously. This uses `locust` with the `websocket-client` library to properly test raw WebSocket connections (not HTTP).

### 1. Install Required Packages

```bash
pip install locust websocket-client
```

> **Note:** Do NOT install `locust-websocket` or other third-party WS plugins. They are often outdated. Using `websocket-client` directly inside Locust tasks gives you full control over binary/text frames and accurate latency reporting.

### 2. Locust Test File (`locustfile.py`)

```python
import json
import time
import gevent
from locust import User, task, events, between
from websocket import create_connection, WebSocketException


class WebSocketUser(User):
    """Custom Locust User for raw WebSocket testing."""
    
    abstract = True  # Prevents this base class from being spawned directly
    
    host = "ws://localhost:8080"
    
    def on_start(self):
        """Establish WS connection when user spawns."""
        try:
            self.ws = create_connection(
                self.host,
                timeout=10,
                # Match server config: no compression for local perf
                enable_multithread=True,
            )
            # Consume the welcome message
            welcome = self.ws.recv()
            self.client_id = json.loads(welcome).get("clientId", "unknown")
        except Exception as e:
            events.user_error.fire(user_instance=self, exception=e, tb=e.__traceback__)
            raise

    def on_stop(self):
        """Cleanly close connection when user stops."""
        if hasattr(self, 'ws') and self.ws.connected:
            self.ws.close()

    def _send_and_receive(self, payload: dict, label: str):
        """
        Wrapper that sends a JSON message, waits for response,
        and reports metrics to Locust dashboard.
        """
        start_time = time.time()
        try:
            self.ws.send(json.dumps(payload))
            response = self.ws.recv()
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            events.request.fire(
                request_type="WS",
                name=label,
                response_time=elapsed_ms,
                response_length=len(response),
                exception=None,
            )
            return json.loads(response)
            
        except WebSocketException as e:
            elapsed_ms = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="WS",
                name=label,
                response_time=elapsed_ms,
                response_length=0,
                exception=e,
            )
            # Reconnect on failure so subsequent tasks don't cascade fail
            self.on_stop()
            self.on_start()
            return None


class EchoUser(WebSocketUser):
    """Tests basic echo/round-trip latency."""
    weight = 3  # 3x more likely to spawn than BroadcastUser
    
    @task
    def ping_pong(self):
        self._send_and_receive({"type": "ping"}, "ping-pong")
    
    @task
    def echo_json(self):
        self._send_and_receive(
            {"type": "echo-test", data": "x" * 256},
            "echo-256b"
        )


class BroadcastUser(WebSocketUser):
    """Tests fan-out broadcast performance under load."""
    weight = 1
    
    @task
    def broadcast_message(self):
        self._send_and_receive(
            {"type": "broadcast", payload": "load-test-broadcast"},
            "broadcast-send"
        )
        # Small sleep to avoid flooding; broadcasts are expensive at scale
        gevent.sleep(0.1)


class BinaryUser(WebSocketUser):
    """Tests binary frame throughput."""
    weight = 1
    
    @task
    def send_binary(self):
        start_time = time.time()
        try:
            # Send 4KB binary payload
            binary_data = b'\x00\x01\x02\x03' * 1024
            self.ws.send(binary_data, opcode=2)  # opcode 2 = binary
            response = self.ws.recv()
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            events.request.fire(
                request_type="WS-BIN",
                name="binary-4kb-echo",
                response_time=elapsed_ms,
                response_length=len(response),
                exception=None,
            )
        except WebSocketException as e:
            elapsed_ms = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="WS-BIN",
                name="binary-4kb-echo",
                response_time=elapsed_ms,
                response_length=0,
                exception=e,
            )
```

### 3. Run the Tests

#### Headless Mode (Recommended for Benchmarking)
```bash
locust -f locustfile.py \
  --headless \
  --users 100 \
  --spawn-rate 20 \
  --run-time 60s \
  --host ws://localhost:8080 \
  --csv=results \
  --html=report.html
```

| Flag | Purpose |
| :--- | :--- |
| `--users 100` | Simulates 100 concurrent WS connections |
| `--spawn-rate 20` | Adds 20 users/sec (prevents connection storm) |
| `--run-time 60s` | Auto-stops after 60 seconds |
| `--csv=results` | Exports `_stats.csv`, `_failures.csv`, `_history.csv` |
| `--html=report.html` | Generates visual performance report |

#### Web UI Mode (For Interactive Exploration)
```bash
locust -f locustfile.py --host ws://localhost:8080
# Open http://localhost:8089 in browser
```

### 4. Key Design Decisions Explained

**Why custom `WebSocketUser` instead of `HttpUser`?**
Locust's built-in `HttpUser` only tracks HTTP requests. Raw WebSocket messages would be invisible in the dashboard. By extending `User` directly and firing `events.request` manually, every WS message appears as a tracked endpoint with proper RPS, latency percentiles, and failure rates.

**Why `gevent.sleep()` in BroadcastUser?**
The Node.js server broadcasts to *all* connected clients. With 100 users each broadcasting continuously, message volume grows quadratically (N²). The small sleep prevents the test from measuring client-side backpressure instead of actual server performance. Adjust or remove based on your real-world usage pattern.

**Why reconnect in `_send_and_receive` exception handler?**
WebSocket connections are stateful and fragile. Without reconnection logic, a single dropped connection causes all subsequent tasks for that user to fail, skewing failure rate metrics. The reconnect ensures failures represent genuine server issues, not transient network blips.

**Why separate User classes with weights?**
Real workloads are mixed. The `weight` attribute lets you model realistic traffic ratios (e.g., 75% echo/ping, 15% broadcast, 10% binary) without complex conditional logic inside tasks.

### 5. Interpreting Results

After running, check these key metrics in `results_stats.csv` or the HTML report:

| Metric | Healthy Threshold (Local) | What It Means If High |
| :--- | :--- | :--- |
| `ping-pong` p99 | < 2ms | Event loop blocking or GC pauses |
| `echo-256b` p99 | < 3ms | JSON parse/serialize bottleneck |
| `broadcast-send` p99 | < 10ms (at 100 users) | O(N) fan-out scaling issue |
| `binary-4kb-echo` p99 | < 5ms | Buffer allocation / copy overhead |
| Failure Rate | < 0.1% | Connection limits or unhandled errors |

> ⚠️ **Important:** Always run Locust on a **separate machine or at minimum a separate CPU core** from the Node.js server. Running both on the same core will cause resource contention and produce misleadingly poor benchmarks. For true local benchmarking, use `taskset` or Docker CPU pinning to isolate processes.