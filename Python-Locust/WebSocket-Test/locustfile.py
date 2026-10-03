import json
import time
import gevent
from locust import User, task, events
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
            {"type": "echo-test", "data": "x" * 256},
            "echo-256b"
        )


class BroadcastUser(WebSocketUser):
    """Tests fan-out broadcast performance under load."""
    weight = 1
    
    @task
    def broadcast_message(self):
        self._send_and_receive(
            {"type": "broadcast", "payload": "load-test-broadcast"},
            "broadcast-send"
        )
        # Small sleep to avoid flooding; broadcasts are expensive at scale
        gevent.sleep(0.2)


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