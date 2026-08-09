You can perform **Spike Testing with Locust** by suddenly increasing the number of simulated users after a stable baseline, holding the spike for a short time, then dropping back down and observing recovery.

The cleanest way is to use a **custom LoadTestShape**.

---

## 1. What is Spike Testing?

Spike testing checks how your system behaves when traffic increases very quickly.

Example:

```text
Normal traffic: 50 users
Suddenly:       5,000 users for 1 minute
Then:           back to 50 users
```

You usually want to verify:

- Does the system survive the sudden burst?
- Does autoscaling react fast enough?
- Do queues grow too much?
- Do database connections exhaust?
- Do error rates increase?
- Does latency recover after the spike?
- Do rate limiters, circuit breakers, or caching layers behave correctly?

---

# 2. Spike Testing with Locust using `LoadTestShape`

Locust allows you to define time-based load profiles using `LoadTestShape`.

Create a file like `spike_locust.py`:

```python
from locust import HttpUser, task, between
from locust.shape import LoadTestShape


class SpikeShape(LoadTestShape):
    """
    Each stage duration is the absolute end time in seconds,
    not the length of the stage.
    """

    stages = [
        # Baseline load
        {"duration": 30,  "users": 50,   "spawn_rate": 10},

        # Spike up very quickly
        {"duration": 40,  "users": 5000, "spawn_rate": 1000},

        # Hold spike load
        {"duration": 100, "users": 5000, "spawn_rate": 1000},

        # Drop back down quickly
        {"duration": 110, "users": 50,   "spawn_rate": 1000},

        # Recovery period
        {"duration": 180, "users": 50,   "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        # Returning None stops the test
        return None


class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def home(self):
        self.client.get("/", name="/home")

    @task(3)
    def api(self):
        self.client.get("/api/items", name="/api/items")
```

Run it headless:

```bash
locust -f spike_locust.py \
  --host=https://staging.example.com \
  --headless \
  --html=spike_report.html \
  --csv=spike_results
```

The shape above does this:

```text
0s    - 30s    baseline: 50 users
30s   - 40s    spike from 50 to 5000 users
40s   - 100s   hold 5000 users
100s  - 110s   drop back to 50 users
110s  - 180s   recovery at 50 users
```

---

# 3. Important detail: `duration` is absolute time

A common mistake is thinking `duration` means “length of this stage”.

In this example:

```python
stages = [
    {"duration": 30,  "users": 50,   "spawn_rate": 10},
    {"duration": 40,  "users": 5000, "spawn_rate": 1000},
]
```

It means:

- From `0s` to `30s`: 50 users
- From `30s` to `40s`: 5000 users

Not:

- 30 seconds at 50 users
- then another 40 seconds at 5000 users

If you want stage lengths, calculate cumulative end times.

---

# 4. Alternative: spike manually using Locust Web API

If you are not using a custom shape, you can start Locust with the web UI and manually change the user count.

Start Locust:

```bash
locust -f locustfile.py --host=https://staging.example.com
```

Then use the swarm endpoint:

```bash
# Baseline
curl -X POST http://localhost:8089/swarm \
  -d "user_count=50&spawn_rate=10"

sleep 30

# Spike
curl -X POST http://localhost:8089/swarm \
  -d "user_count=5000&spawn_rate=1000"

sleep 60

# Recover
curl -X POST http://localhost:8089/swarm \
  -d "user_count=50&spawn_rate=1000"
```

This works, but for repeatable CI/CD tests, a `LoadTestShape` is usually better.

---

# 5. Spike Testing advice for Locust

## 5.1 Decide if you are spiking users or requests per second

Locust is primarily user-based, not directly RPS-based.

If your production traffic spike is measured in requests per second, estimate users using Little’s Law:

```text
users ≈ target_rps × average_response_time
```

Example:

```text
Target spike: 1,000 RPS
Average response time: 0.2s

users ≈ 1000 × 0.2 = 200 users
```

If you use think time or pacing, include it:

```text
users ≈ target_rps × average_cycle_time
```

Where `average_cycle_time` includes:

```text
response time + wait time / pacing
```

---

## 5.2 Use a high `spawn_rate`, but be careful

For a spike, you usually want a high spawn rate:

```python
{"duration": 40, "users": 5000, "spawn_rate": 1000}
```

But very high spawn rates can overload Locust itself.

Watch out for:

- Locust worker CPU saturation
- Too many open sockets
- TLS handshake storms
- DNS resolution delays
- Load generator network limits
- Connection pool exhaustion inside Locust

Before blaming the system under test, verify that Locust itself is not the bottleneck.

---

## 5.3 Use distributed Locust for large spikes

If you need thousands or tens of thousands of users, use master/worker mode.

Master:

```bash
locust -f spike_locust.py --master
```

Workers:

```bash
locust -f spike_locust.py --worker --master-host=<master-ip>
```

For headless:

```bash
locust -f spike_locust.py \
  --master \
  --headless \
  --expect-workers=4
```

The master coordinates the test, while workers generate the load.

---

## 5.4 Use realistic user behavior

A spike test should not usually send requests as fast as possible unless that is your real traffic pattern.

Use wait times:

```python
from locust import between

class ApiUser(HttpUser):
    wait_time = between(1, 3)
```

Or pacing:

```python
from locust import constant_pacing

class ApiUser(HttpUser):
    wait_time = constant_pacing(2)
```

`constant_pacing(2)` means each user tries to start one request every 2 seconds.

---

## 5.5 Separate spike scenarios from capacity scenarios

A spike test is not always the same as a max-capacity test.

For spike testing, you may keep realistic think time.

For stress or capacity testing, you may reduce or remove think time to find the breaking point.

Example:

```python
wait_time = between(0, 0)
```

But if you remove think time, clearly label the test as artificial capacity testing, not realistic user load.

---

## 5.6 Monitor the system during the spike

Locust metrics alone are not enough.

During the spike, monitor:

- HTTP status codes
- p50, p95, p99 latency
- error rate
- CPU and memory
- database connections
- database lock waits
- connection pool usage
- thread pool usage
- queue depth
- autoscaling events
- cache hit ratio
- GC pauses
- network saturation
- load balancer health
- retry storms

A spike test is most useful when you can connect Locust metrics to backend metrics.

---

## 5.7 Define pass/fail criteria

Example spike-test success criteria:

```text
Error rate < 1%
p95 latency < 800ms
p99 latency < 2s
No HTTP 5xx burst longer than 30 seconds
System recovers within 2 minutes after spike
No data corruption
No queue backlog older than 5 minutes
```

Without thresholds, spike tests become subjective.

---

## 5.8 Test recovery, not just survival

A good spike test includes recovery time.

Example shape:

```text
Baseline
Spike
Hold spike
Drop to baseline
Observe recovery
```

This is important for autoscaling systems because they may survive the spike but recover poorly afterward.

---

# 6. Stress Testing with Locust

Stress testing means increasing load gradually until the system breaks or performance becomes unacceptable.

The goal is to find:

- maximum capacity
- breaking point
- failure mode
- whether degradation is graceful
- how the system recovers

---

## Example stress-test shape

Save as `stress_locust.py`:

```python
from locust import HttpUser, task, between
from locust.shape import LoadTestShape


class StressShape(LoadTestShape):
    stages = [
        {"duration": 60,  "users": 100,  "spawn_rate": 20},
        {"duration": 120, "users": 300,  "spawn_rate": 40},
        {"duration": 180, "users": 600,  "spawn_rate": 80},
        {"duration": 240, "users": 1200, "spawn_rate": 160},
        {"duration": 300, "users": 2400, "spawn_rate": 320},
        {"duration": 360, "users": 4800, "spawn_rate": 640},
        {"duration": 420, "users": 9600, "spawn_rate": 1200},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None


class ApiUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def endpoint(self):
        self.client.get("/api/items", name="/api/items")
```

Run:

```bash
locust -f stress_locust.py \
  --host=https://staging.example.com \
  --headless \
  --html=stress_report.html \
  --csv=stress_results
```

---

## Stress testing advice

### Increase load in steps

Do not jump immediately to extreme load unless you are doing spike testing.

Good stress pattern:

```text
100 users
300 users
600 users
1200 users
2400 users
4800 users
```

Hold each step long enough to observe:

- latency stabilization
- autoscaling behavior
- cache warmup
- database pressure
- memory growth
- queue growth

---

### Look for the hockey stick

You are usually looking for the point where latency starts rising sharply.

Example:

```text
Users    p95 latency
100      120ms
300      140ms
600      180ms
1200     350ms
2400     1200ms
4800     6000ms
```

The breaking point is often between 1200 and 2400 users.

---

### Watch error type

Different errors mean different things:

| Error | Possible cause |
|---|---|
| Connection timeout | Load balancer, network, server accept queue |
| Read timeout | Slow backend processing |
| HTTP 502/503 | Service unavailable, crashed pods, exhausted workers |
| HTTP 429 | Rate limiting |
| Connection refused | Server cannot accept new connections |
| DB errors | Connection pool exhaustion, locks, deadlocks |

---

### Test graceful degradation

A system may fail, but it should fail gracefully.

Check:

- Are critical endpoints still available?
- Are non-critical features disabled?
- Are users getting meaningful errors?
- Does the system recover when load decreases?
- Are queued jobs processed eventually?

---

# 7. Other Types of Testing You Can Do with Locust

## 7.1 Smoke Testing

Purpose: verify that the test script and environment work.

Example:

```bash
locust -f locustfile.py \
  --host=https://staging.example.com \
  --headless \
  --users=2 \
  --spawn-rate=1 \
  --run-time=30s
```

Advice:

- Use very few users.
- Run for a short time.
- Test all critical endpoints.
- Verify authentication, headers, test data, and environment access.
- Run this before every larger test.

---

## 7.2 Load Testing

Purpose: validate expected normal or peak traffic.

Example:

```python
from locust.shape import LoadTestShape


class LoadTestShapeExample(LoadTestShape):
    stages = [
        {"duration": 60,  "users": 100, "spawn_rate": 10},
        {"duration": 300, "users": 500, "spawn_rate": 20},
        {"duration": 360, "users": 100, "spawn_rate": 50},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
```

Advice:

- Use expected production traffic.
- Use realistic user journeys.
- Use realistic think time.
- Use production-like data volume.
- Define SLOs, for example:

```text
p95 < 500ms
error rate < 0.5%
CPU < 70%
DB connections < 80% of max
```

---

## 7.3 Soak / Endurance Testing

Purpose: find memory leaks, connection leaks, queue growth, and resource exhaustion over time.

Example:

```bash
locust -f locustfile.py \
  --host=https://staging.example.com \
  --headless \
  --users=300 \
  --spawn-rate=20 \
  --run-time=8h \
  --csv=soak_results \
  --html=soak_report.html
```

Advice:

- Use moderate load, often 50% to 70% of expected capacity.
- Run for hours or days.
- Watch memory growth.
- Watch file descriptors.
- watch database connections.
- Watch log file growth.
- Watch queue backlog.
- Watch token expiration and renewal issues.
- Watch scheduled jobs and batch effects.

---

## 7.4 Peak Testing

Purpose: simulate busy periods, such as morning login bursts, flash sales, or event-driven traffic.

Example:

```text
Baseline: 100 users
Morning peak: 3,000 users for 10 minutes
Return to baseline
Evening peak: 5,000 users for 10 minutes
Return to baseline
```

Advice:

- Use repeated peak patterns.
- Test scale-up and scale-down.
- Check whether caches remain warm.
- Check whether connection pools recover.
- Check whether background jobs catch up.

---

## 7.5 Capacity Testing

Purpose: determine the maximum sustainable traffic level.

Approach:

```text
Run 1: 500 users
Run 2: 1000 users
Run 3: 1500 users
Run 4: 2000 users
Run 5: 2500 users
```

For each run, record:

```text
RPS
p50
p95
p99
error rate
CPU
memory
DB connections
queue depth
```

Advice:

- Increase load gradually.
- Hold each level long enough to stabilize.
- Stop when SLOs are violated.
- Do not only measure maximum RPS; measure sustainable RPS.

---

## 7.6 Scalability Testing

Purpose: verify whether adding resources increases throughput.

Example:

```text
1 instance:  1000 RPS
2 instances: 1900 RPS
4 instances: 3400 RPS
8 instances: 5000 RPS
```

If doubling instances does not roughly double throughput, you may have a shared bottleneck:

- database
- cache
- message broker
- external API
- load balancer
- locks
- network
- storage

Advice:

- Keep Locust load generators out of the bottleneck.
- Use multiple Locust workers.
- Run the same Locust script for each backend size.
- Compare results using the same user behavior and data.

---

# 8. Optional: Make Locust fail CI when SLOs are violated

You can add a listener to set a non-zero exit code when thresholds are not met.

```python
from locust import events


@events.quitting.add_listener
def check_slo(environment, **kwargs):
    total = environment.stats.total

    if total.num_requests == 0:
        environment.process_exit_code = 1
        return

    failure_ratio = total.num_failures / total.num_requests
    p95 = total.get_response_time_percentile(0.95) or 0

    max_failure_ratio = 0.01
    max_p95_ms = 800

    if failure_ratio > max_failure_ratio or p95 > max_p95_ms:
        print(
            f"SLO failed: failure_ratio={failure_ratio:.4f}, "
            f"p95={p95}ms"
        )
        environment.process_exit_code = 1
    else:
        print(
            f"SLO passed: failure_ratio={failure_ratio:.4f}, "
            f"p95={p95}ms"
        )
        environment.process_exit_code = 0
```

Then run:

```bash
locust -f locustfile.py \
  --host=https://staging.example.com \
  --headless \
  --users=500 \
  --spawn-rate=20 \
  --run-time=5m
```

If the SLO fails, Locust exits with code 1, which is useful in CI pipelines.

---

# 9. Practical Locust command examples

## Smoke test

```bash
locust -f locustfile.py --headless -u 2 -r 1 -t 30s
```

## Simple load test

```bash
locust -f locustfile.py --headless -u 500 -r 20 -t 10m
```

## Stress test using repeated runs

```bash
for users in 100 250 500 1000 2000 4000; do
  locust -f locustfile.py \
    --headless \
    -u $users \
    -r 100 \
    -t 5m \
    --csv=stress_${users}_users \
    --html=stress_${users}_users.html
done
```

## Distributed master

```bash
locust -f locustfile.py --master
```

## Distributed worker

```bash
locust -f locustfile.py --worker --master-host=10.0.0.10
```

## Generate reports

```bash
locust -f locustfile.py \
  --headless \
  -u 1000 \
  -r 50 \
  -t 10m \
  --csv=results/run \
  --html=results/report.html
```

This creates files like:

```text
results/run_stats.csv
results/run_failures.csv
results/run_stats_history.csv
results/report.html
```

---

# 10. Common mistakes to avoid

## Mistake 1: Using too high spawn rate without checking Locust capacity

If Locust cannot spawn users fast enough, your spike will not be real.

Check:

- Locust CPU
- Locust memory
- open connections
- network usage
- worker logs

---

## Mistake 2: Testing only one endpoint

Real traffic usually touches multiple endpoints.

Use task weights:

```python
from locust import HttpUser, task

class WebUser(HttpUser):
    @task(5)
    def home(self):
        self.client.get("/")

    @task(2)
    def search(self):
        self.client.get("/search")

    @task(1)
    def checkout(self):
        self.client.post("/checkout")
```

---

## Mistake 3: Using the same test data repeatedly

This can produce unrealistic cache behavior.

Use parameterized data:

```python
import random

ids = range(1, 10000)

class ApiUser(HttpUser):
    @task
    def get_item(self):
        item_id = random.choice(ids)
        self.client.get(f"/api/items/{item_id}", name="/api/items/[id]")
```

---

## Mistake 4: Ignoring connection reuse

Real browsers and mobile apps often reuse connections.

If your Locust test creates a new TLS connection for every request, it may over-test TLS handshake capacity and under-test real behavior.

Consider:

- keep-alive
- connection pooling
- realistic client behavior
- `FastHttpUser` for high-load HTTP tests

Example:

```python
from locust.contrib.fasthttp import FastHttpUser
from locust import task, between


class ApiUser(FastHttpUser):
    wait_time = between(1, 3)

    @task
    def home(self):
        self.client.get("/")
```

---

## Mistake 5: Only measuring average latency

Average latency hides bad user experience.

Use percentiles:

- p50
- p90
- p95
- p99
- max

A system can have a good average but terrible p99.

---

# 11. Recommended test strategy with Locust

A good progression is:

```text
1. Smoke Test
   Verify script and environment.

2. Baseline Load Test
   Validate normal expected traffic.

3. Spike Test
   Validate sudden traffic bursts and recovery.

4. Stress Test
   Increase load until failure.

5. Capacity Test
   Find maximum sustainable load.

6. Soak Test
   Run moderate load for a long time.

7. Scalability Test
   Compare throughput as infrastructure scales.
```

---

# 12. Summary

For **Spike Testing** in Locust:

- Use a custom `LoadTestShape`.
- Start with a baseline.
- Increase users very quickly.
- Hold the spike briefly.
- Drop back down.
- Observe recovery.
- Use distributed workers for large spikes.
- Monitor backend systems, not only Locust.
- Define pass/fail thresholds.

For **Stress Testing**:

- Increase load gradually.
- Hold each step.
- Find the breaking point.
- Observe failure behavior.
- Test recovery after overload.
- Use Locust reports and backend monitoring together.