In Locust, **tasks** are the core building blocks that define what virtual users will do during a performance test. They represent individual actions or behaviors that users perform on your application.

## What are Tasks?

Tasks are Python methods decorated with `@task` that define user behavior. Each task represents an action like:
- Making HTTP requests
- Browsing pages
- Submitting forms
- API calls

## Basic Task Structure

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    
    @task
    def view_homepage(self):
        self.client.get("/")
    
    @task(3)  # This task is 3x more likely to be executed
    def view_products(self):
        self.client.get("/products")
```

## Separating Performance Testing Logic

### 1. **Organize Tasks by Feature/Module**

```python
from locust import HttpUser, task, between, TaskSet

class AuthTaskSet(TaskSet):
    """Authentication-related tasks"""
    
    @task
    def login(self):
        self.client.post("/login", json={
            "username": "testuser",
            "password": "testpass"
        })
    
    @task
    def logout(self):
        self.client.post("/logout")

class ProductTaskSet(TaskSet):
    """Product-related tasks"""
    
    @task
    def browse_products(self):
        self.client.get("/products")
    
    @task(2)
    def view_product_detail(self):
        product_id = 123
        self.client.get(f"/products/{product_id}")

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)
    tasks = [AuthTaskSet, ProductTaskSet]  # Combine multiple task sets
```

### 2. **Use Separate User Classes for Different User Types**

```python
from locust import HttpUser, task, between

class AdminUser(HttpUser):
    """Simulates admin user behavior"""
    wait_time = between(2, 5)
    
    @task
    def view_dashboard(self):
        self.client.get("/admin/dashboard")
    
    @task
    def manage_users(self):
        self.client.get("/admin/users")

class RegularUser(HttpUser):
    """Simulates regular user behavior"""
    wait_time = between(1, 3)
    
    @task(3)
    def browse_products(self):
        self.client.get("/products")
    
    @task
    def view_cart(self):
        self.client.get("/cart")
```

### 3. **Create Reusable Task Modules**

```python
# tasks/auth_tasks.py
from locust import TaskSet, task

class AuthTasks(TaskSet):
    @task
    def login(self):
        response = self.client.post("/api/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")

# tasks/product_tasks.py
from locust import TaskSet, task

class ProductTasks(TaskSet):
    @task
    def list_products(self):
        self.client.get("/api/products")
    
    @task(2)
    def search_products(self):
        self.client.get("/api/products/search?q=laptop")

# main_locustfile.py
from locust import HttpUser, between
from tasks.auth_tasks import AuthTasks
from tasks.product_tasks import ProductTasks

class ApiUser(HttpUser):
    wait_time = between(1, 4)
    tasks = [AuthTasks, ProductTasks]
```

## Using Tasks with Locust HTTP Client

The `self.client` in HttpUser provides an HTTP client with built-in request tracking:

```python
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    host = "http://localhost:3000"
    wait_time = between(1, 3)
    
    @task
    def get_users(self):
        # Basic GET request
        response = self.client.get("/api/users")
        
        # With custom name for better reporting
        response = self.client.get("/api/users/123", name="/api/users/[id]")
        
        # Check response and handle errors
        if response.status_code != 200:
            print(f"Failed: {response.status_code}")
    
    @task
    def create_user(self):
        # POST request with JSON data
        response = self.client.post("/api/users", 
                                   json={
                                       "name": "John Doe",
                                       "email": "john@example.com"
                                   },
                                   headers={"Content-Type": "application/json"})
        
        # Validate response
        assert response.status_code == 201
    
    @task
    def update_user(self):
        # PUT request
        response = self.client.put("/api/users/123",
                                  json={"name": "Jane Doe"},
                                  name="/api/users/[id]/update")
    
    @task
    def delete_user(self):
        # DELETE request
        response = self.client.delete("/api/users/123",
                                     name="/api/users/[id]/delete")
```

## Advanced Task Features

### Weighted Tasks
```python
class WeightedUser(HttpUser):
    @task(1)
    def rare_action(self):
        self.client.get("/rare-page")
    
    @task(5)
    def common_action(self):
        self.client.get("/common-page")
```

### Sequential Tasks with `@tag`
```python
from locust import HttpUser, task, tag

class TaggedUser(HttpUser):
    @task
    @tag("critical")
    def critical_path(self):
        self.client.get("/checkout")
    
    @task
    @tag("smoke")
    def smoke_test(self):
        self.client.get("/")
```

### Dynamic Task Selection
```python
class SmartUser(HttpUser):
    def on_start(self):
        """Called when a user starts"""
        self.login()
    
    def login(self):
        response = self.client.post("/login", json={
            "username": "user",
            "password": "pass"
        })
        self.token = response.json().get("token")
    
    @task
    def authenticated_request(self):
        self.client.get("/protected", 
                       headers={"Authorization": f"Bearer {self.token}"})
```

## Running Tests with Specific Tasks

```bash
# Run all tasks
locust -f locustfile.py

# Run specific user class
locust -f locustfile.py --users 10 --spawn-rate 2

# Filter by tags
locust -f locustfile.py --tags critical smoke
```

This separation approach makes your tests modular, maintainable, and easier to understand!