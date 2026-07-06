Sharing data between tasks in Locust is essential for simulating realistic user flows (e.g., logging in to get a token, then using that token in subsequent requests). Since each virtual user is an independent instance of your User class, there are several ways to share state.

Here are the most common and effective methods:

## 1. Using Instance Attributes (`self`)

The simplest way is to store data as attributes of the user instance. This data persists across all tasks executed by that specific virtual user.

```python
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def login_and_store_token(self):
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "secret"
        })
        if response.status_code == 200:
            # Store token in instance attribute
            self.auth_token = response.json().get("token")
            self.user_id = response.json().get("user_id")
            print(f"User {self.user_id} logged in")
    
    @task
    def use_stored_token(self):
        # Check if token exists before using it
        if hasattr(self, 'auth_token'):
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            self.client.get("/protected-resource", headers=headers)
        else:
            print("No token found, skipping request")
```

**Pros:** Simple, isolated per user.
**Cons:** Data is not shared between different virtual users.

## 2. Using `on_start` for Initialization

If you need data available from the very first task, use `on_start`. This method runs once when the user starts.

```python
from locust import HttpUser, task, between

class InitializedUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called once when the user starts"""
        # Perform login and store credentials
        response = self.client.post("/login", json={
            "username": "user",
            "password": "pass"
        })
        self.token = response.json().get("token")
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task
    def protected_request_1(self):
        self.client.get("/dashboard", headers=self.headers)
    
    @task
    def protected_request_2(self):
        self.client.get("/profile", headers=self.headers)
```

## 3. Sharing Data Between Different Virtual Users

If you need to share data across *all* virtual users (e.g., a list of valid product IDs), you can use class-level variables or external storage.

### A. Class-Level Variables

```python
import random
from locust import HttpUser, task, between

class SharedDataUser(HttpUser):
    wait_time = between(1, 3)
    
    # Class-level variable shared by all instances
    product_ids = [101, 102, 103, 104, 105]
    
    @task
    def view_random_product(self):
        # All users access the same list
        product_id = random.choice(self.product_ids)
        self.client.get(f"/products/{product_id}")
```

### B. Using `environment` Object

Locust provides an `environment` object that can hold shared state.

```python
from locust import HttpUser, task, between, events

def init_shared_data(environment):
    """Initialize shared data before test starts"""
    environment.shared_data = {
        "valid_usernames": ["user1", "user2", "user3"],
        "api_key": "shared-secret-key"
    }

events.init.add_listener(init_shared_data)

class EnvSharedUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def use_shared_data(self):
        # Access shared data from environment
        usernames = self.environment.shared_data["valid_usernames"]
        username = usernames[0]  # Or pick randomly
        
        self.client.get(f"/users/{username}")
```

## 4. Using External Storage (Redis/Database)

For complex scenarios or distributed tests, use an external store.

```python
import redis
from locust import HttpUser, task, between

# Connect to Redis (ensure redis-py is installed)
r = redis.Redis(host='localhost', port=6379, db=0)

class RedisSharedUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_shared_counter(self):
        # Increment a shared counter
        count = r.incr("test_counter")
        self.client.get(f"/status?request_number={count}")
    
    @task
    def use_shared_list(self):
        # Get a random item from a shared list
        item = r.lpop("test_items")
        if item:
            self.client.get(f"/items/{item.decode()}")
```

## 5. Passing Data Between Tasks in a Sequence

When using `TaskSet` or sequential tasks, you can pass data explicitly.

```python
from locust import HttpUser, TaskSet, task, seq_task, between

class UserJourney(TaskSet):
    
    @seq_task(1)
    def login(self):
        response = self.client.post("/login", json={"user": "test", "pass": "test"})
        # Store in parent user instance
        self.user.token = response.json().get("token")
    
    @seq_task(2)
    def create_order(self):
        # Use token from previous step
        headers = {"Authorization": f"Bearer {self.user.token}"}
        response = self.client.post("/orders", json={"item": "laptop"}, headers=headers)
        
        # Store order ID for next step
        self.order_id = response.json().get("order_id")
    
    @seq_task(3)
    def check_order_status(self):
        # Use order ID from previous step
        headers = {"Authorization": f"Bearer {self.user.token}"}
        self.client.get(f"/orders/{self.order_id}", headers=headers)

class SequentialUser(HttpUser):
    wait_time = between(1, 3)
    tasks = [UserJourney]
```

## Best Practices for Sharing Data

1. **Use `self` for per-user state**: Most common and safest.
2. **Use `on_start` for setup**: Ensures data is ready before tasks run.
3. **Check for existence**: Always check if data exists before using it (`hasattr` or `try/except`).
4. **Avoid global mutable state**: Can lead to race conditions in distributed tests.
5. **Use external stores for cross-user data**: Redis is excellent for this.
6. **Keep it simple**: Don't over-engineer; start with instance attributes.

## Example: Complete Realistic Flow

```python
from locust import HttpUser, task, between

class EcommerceUser(HttpUser):
    wait_time = between(2, 5)
    
    def on_start(self):
        # 1. Login and get token
        res = self.client.post("/login", json={"user": "shopper", "pass": "123"})
        self.token = res.json().get("token")
        
        # 2. Get a list of products
        res = self.client.get("/products", headers={"Auth": self.token})
        self.product_ids = [p['id'] for p in res.json().get('products', [])]
    
    @task(3)
    def browse_products(self):
        if self.product_ids:
            pid = self.product_ids[0]
            self.client.get(f"/products/{pid}", headers={"Auth": self.token})
    
    @task(1)
    def add_to_cart(self):
        if self.product_ids:
            pid = self.product_ids[0]
            self.client.post("/cart/add", json={"product_id": pid}, headers={"Auth": self.token})
    
    @task(1)
    def checkout(self):
        self.client.post("/checkout", headers={"Auth": self.token})
```

This approach ensures that each user has their own session data, mimicking real-world behavior accurately.