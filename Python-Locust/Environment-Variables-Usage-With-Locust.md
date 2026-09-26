You can use environment variables in Locust tasks to make your tests more flexible and configurable. Here are several approaches:

## 1. **Accessing Environment Variables Directly**

```python
import os
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)
    
    # Get environment variables at class level
    BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
    API_KEY = os.getenv("API_KEY", "default-key")
    USERNAME = os.getenv("TEST_USERNAME", "testuser")
    PASSWORD = os.getenv("TEST_PASSWORD", "testpass")
    
    @task
    def authenticated_request(self):
        response = self.client.get("/api/data", 
                                   headers={
                                       "Authorization": f"Bearer {self.API_KEY}",
                                       "X-API-Key": self.API_KEY
                                   })
    
    @task
    def login_with_env_credentials(self):
        response = self.client.post("/login", json={
            "username": self.USERNAME,
            "password": self.PASSWORD
        })
```

## 2. **Using `on_start` for Initialization**

```python
import os
from locust import HttpUser, task, between

class ConfigurableUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called once when the user starts"""
        # Load environment variables
        self.base_url = os.getenv("BASE_URL", "http://localhost:3000")
        self.api_key = os.getenv("API_KEY")
        self.username = os.getenv("USERNAME", "admin")
        self.password = os.getenv("PASSWORD", "secret")
        self.environment = os.getenv("ENVIRONMENT", "staging")
        
        # Perform initial setup
        if self.api_key:
            self.login()
    
    def login(self):
        """Login using credentials from environment"""
        response = self.client.post("/auth/login", json={
            "username": self.username,
            "password": self.password,
            "api_key": self.api_key
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
    
    @task
    def fetch_data(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/data", headers=headers)
```

## 3. **Using Locust's Built-in Environment Variables**

Locust provides several built-in environment variables you can access:

```python
from locust import HttpUser, task, between, events

class SmartUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Access Locust's internal settings
        print(f"Host: {self.host}")
        print(f"Number of users: {self.environment.runner.user_count if self.environment.runner else 'N/A'}")
    
    @task
    def dynamic_request(self):
        # Use environment-specific endpoints
        env = os.getenv("ENVIRONMENT", "dev")
        
        if env == "production":
            endpoint = "/api/v2/data"
        elif env == "staging":
            endpoint = "/api/v1/data"
        else:
            endpoint = "/api/dev/data"
        
        self.client.get(endpoint)
```

## 4. **Loading Configuration from `.env` File**

First, install python-dotenv:
```bash
pip install python-dotenv
```

Then use it in your Locust file:

```python
import os
from dotenv import load_dotenv
from locust import HttpUser, task, between

# Load .env file
load_dotenv()

class EnvConfiguredUser(HttpUser):
    wait_time = between(1, 3)
    
    # Configuration from .env file
    HOST = os.getenv("LOCUST_HOST", "http://localhost:8000")
    NUM_USERS = int(os.getenv("NUM_USERS", "10"))
    SPAWN_RATE = int(os.getenv("SPAWN_RATE", "2"))
    API_TOKEN = os.getenv("API_TOKEN")
    
    def on_start(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json"
        }
    
    @task
    def get_profile(self):
        self.client.get("/api/profile", headers=self.headers)
    
    @task(2)
    def update_profile(self):
        self.client.put("/api/profile", 
                       json={"name": "Test User"},
                       headers=self.headers)
```

Example `.env` file:
```env
LOCUST_HOST=http://staging.example.com
NUM_USERS=50
SPAWN_RATE=5
API_TOKEN=your-secret-token-here
TEST_USERNAME=testuser@example.com
TEST_PASSWORD=securepassword123
ENVIRONMENT=staging
```

## 5. **Using Command-Line Arguments with Environment Variables**

```python
import os
from locust import HttpUser, task, between, events

# Parse custom command-line arguments
def parse_options(environment):
    parser = environment.parsed_options
    # You can add custom arguments here
    return parser

class FlexibleUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Combine env vars with defaults
        self.config = {
            "base_url": os.getenv("BASE_URL", self.host),
            "api_version": os.getenv("API_VERSION", "v1"),
            "timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
            "retry_count": int(os.getenv("RETRY_COUNT", "3"))
        }
    
    @task
    def versioned_api_call(self):
        version = self.config["api_version"]
        endpoint = f"/api/{version}/users"
        
        response = self.client.get(
            endpoint,
            timeout=self.config["timeout"]
        )
```

Run with:
```bash
export BASE_URL=http://api.example.com
export API_VERSION=v2
export REQUEST_TIMEOUT=60
locust -f locustfile.py
```

## 6. **Environment-Specific Task Sets**

```python
import os
from locust import HttpUser, TaskSet, task, between

class DevTasks(TaskSet):
    @task
    def debug_endpoint(self):
        self.client.get("/debug/info")
    
    @task
    def test_data(self):
        self.client.get("/test-data")

class ProdTasks(TaskSet):
    @task
    def main_feature(self):
        self.client.get("/api/main-feature")
    
    @task(3)
    def critical_path(self):
        self.client.get("/api/checkout")

class EnvironmentAwareUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        env = os.getenv("ENVIRONMENT", "dev").lower()
        
        if env == "production":
            self.tasks = [ProdTasks]
        elif env == "staging":
            self.tasks = [ProdTasks]  # Similar to prod
        else:
            self.tasks = [DevTasks]  # Default to dev
        
        print(f"Running with environment: {env}")
```

## 7. **Using Environment Variables for Data-Driven Testing**

```python
import os
import json
from locust import HttpUser, task, between

class DataDrivenUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Load test data from environment variable (JSON string)
        test_data_json = os.getenv("TEST_DATA")
        if test_data_json:
            self.test_data = json.loads(test_data_json)
        else:
            # Default test data
            self.test_data = [
                {"id": 1, "name": "Product 1"},
                {"id": 2, "name": "Product 2"}
            ]
    
    @task
    def iterate_test_data(self):
        for item in self.test_data:
            self.client.get(f"/api/products/{item['id']}")
```

Run with:
```bash
export TEST_DATA='[{"id": 101, "name": "Laptop"}, {"id": 102, "name": "Phone"}]'
locust -f locustfile.py
```

## Best Practices

1. **Provide sensible defaults** - Always have fallback values
2. **Validate required variables** - Check if critical env vars are set
3. **Use `.env` files for local development** - Keep secrets out of code
4. **Document required variables** - Add comments or a README
5. **Don't hardcode secrets** - Use environment variables for tokens, passwords, etc.

Example validation:
```python
def on_start(self):
    required_vars = ["API_KEY", "BASE_URL"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
    
    self.api_key = os.getenv("API_KEY")
```

This approach makes your Locust tests portable across different environments (dev, staging, production) without modifying the code!