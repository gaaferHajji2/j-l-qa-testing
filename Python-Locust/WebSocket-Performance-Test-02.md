Here is a complete Locust performance test suite tailored specifically for the `ws` server created previously.

### 1. Install Required Packages

Locust does not include a WebSocket client by default. You need the community-maintained plugin:

```bash
pip install locust locust-plugins
```

> **Note:** `locust-plugins` provides the `WebSocketUser` base class which properly integrates WS events with Locust's statistics engine. Do not use raw `websockets` library directly, as it won't report metrics to the Locust dashboard.

### 2. The Locust Test File (`locustfile.py`)

This test covers three scenarios matching the server's message handlers: latency pings, JSON echo, and broadcast fan-out.

```python
import json
import time
from locust import task, events
from locust_plugins.users import WebSocketUser


class WsPerformanceUser(WebSocketUser):
    """
    Performance test user for the Node.js ws server.
    Connects once per user and reuses the connection for all tasks.
    """
    
    # Target the local ws server
    host = "ws://localhost:8080"
    
    # Connection-level config
    abstract = False
    
    def on_start(self):
        """Called when a virtual user starts. Wait for welcome message."""
        # Block until we receive the welcome message to ensure connection is ready
        welcome = self.ws.recv()
        data = json.loads(welcome)
        if data.get("type") != "welcome":
            raise Exception(f"Unexpected welcome message: {data}")
        self.client_id = data.get("clientId")

    @task(3)
    def ping_latency(self):
        """Measure round-trip latency using the server's ping/pong handler."""
        payload = json.dumps({"type": "ping"})
        
        start_time = time.time()
        self.ws.send(payload)
        response = self.ws.recv()
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        msg = json.loads(response)
        success = msg.get("type") == "pong"
        
        # Report to Locust stats under a dedicated endpoint name
        events.request.fire(
            request_type="WS",
            name="ping_pong",
            response_time=elapsed_ms,
            response_length=len(response),
            exception=None if success else Exception(f"Expected pong, got {msg}"),
            context={"client_id": self.client_id},
        )

    @task(5)
    def json_echo(self):
        """Test JSON parse/serialize throughput on the server."""
        payload = json.dumps({
            "type": "echo_test",
            "data": {"key": "value", "numbers": list(range(50))},
            "timestamp": time.time(),
        })
        
        start_time = time.time()
        self.ws.send(payload)
        response = self.ws.recv()
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        msg = json.loads(response)
        success = msg.get("type") == "echo"
        
        events.request.fire(
            request_type="WS",
            name="json_echo",
            response_time=elapsed_ms,
            response_length=len(response),
            exception=None if success else Exception(f"Echo mismatch: {msg}"),
        )

    @task(1)
    def broadcast_message(self):
        """
        Send a broadcast message. 
        NOTE: This user will also RECEIVE broadcasts from other users.
        We only measure the send + immediate ack, not fan-out delivery.
        """
        payload = json.dumps({
            "type": "broadcast",
            "data": f"broadcast-from-{self.client_id}",
        })
        
        start_time = time.time()
        self.ws.send(payload)
        # Server doesn't ACK broadcasts, so we just measure send time
        # In production tests, you'd correlate via sequence numbers
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        events.request.fire(
            request_type="WS",
            name="broadcast_send",
            response_time=elapsed_ms,
            response_length=len(payload),
            exception=None,
        )
        
        # Drain any incoming broadcast messages from other users
        # to prevent buffer buildup during high-load tests
        self._drain_incoming()

    def _drain_incoming(self, max_messages=100):
        """Non-blocking drain of buffered incoming messages."""
        drained = 0
        while drained < max_messages:
            try:
                self.ws.settimeout(0.001)
                self.ws.recv()
                drained += 1
            except Exception:
                break
            finally:
                self.ws.settimeout(None)

    def on_stop(self):
        """Clean disconnect when user stops."""
        try:
            self.ws.close()
        except Exception:
            pass
```

### 3. Run the Test

#### Headless Mode (CLI output)
```bash
locust -f locustfile.py \
  --headless \
  --users 100 \
  --spawn-rate 10 \
  --run-time 60s \
  --host ws://localhost:8080
```

#### Web Dashboard Mode
```bash
locust -f locustfile.py --host ws://localhost:8080
```
Then open `http://localhost:8089` in your browser. Set users/spawn rate in the UI.

### 4. Key Design Decisions Explained

| Decision | Rationale |
| :--- | :--- |
| `WebSocketUser` base class | Provides persistent connections. Standard `HttpUser` creates new connections per task, which measures TCP handshake overhead, not WS message throughput. |
| Manual `events.request.fire()` | `locust-plugins` auto-captures send/recv, but grouping by logical operation (`ping_pong`, `json_echo`) gives meaningful percentile charts instead of generic `ws_send`/`ws_recv` noise. |
| Task weights `(3, 5, 1)` | Mirrors realistic traffic: echoes are most common, pings are frequent health checks, broadcasts are rare but expensive. Adjust ratios to match your actual workload. |
| `_drain_incoming()` | Without this, broadcast-heavy tests cause unbounded memory growth as each user accumulates unread messages from all other users. This is the #1 cause of OOM crashes in WS load tests. |
| `settimeout(0.001)` in drain | Non-blocking check. A blocking `recv()` here would stall the greenlet and artificially inflate latency metrics for subsequent tasks. |

### 5. Interpreting Results

After a 60-second test at 100 users, focus on these metrics in the Locust dashboard:

-   **`ping_pong` p50/p99**: Your true server processing latency. For localhost, expect p99 < 2ms.
-   **`json_echo` RPS**: Measures JSON serialization/deserialization throughput. This is typically the CPU bottleneck.
-   **`broadcast_send` p99**: Should remain flat regardless of user count. If it climbs, the server's `forEach` broadcast loop is becoming a bottleneck (consider batching or worker threads).
-   **Failures tab**: Any non-zero failures indicate protocol mismatches or server crashes under load. Check your Node.js server logs immediately.

> ⚠️ **Common Pitfall**: If you see `ConnectionRefusedError` spikes during ramp-up, your OS is exhausting ephemeral ports. Fix with:
> ```bash
> # Linux/macOS temporary fix for local testing
> sudo sysctl -w net.ipv4.ip_local_port_range="1024 65535"
> ulimit -n 65535
> ```