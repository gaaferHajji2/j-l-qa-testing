# Task Weighting vs Task Sequencing in Locust

These are two fundamental concepts that control **how** and **when** tasks are executed by virtual users.

---

## 1. Task Weighting

Task weighting controls the **probability** or **frequency** of task execution. It determines which tasks are more likely to be chosen when a user picks their next action.

### How Weighting Works

By default, all tasks have equal weight (weight = 1). You can change this to make some tasks execute more frequently than others.

### Methods to Define Weights

#### **Method 1: Using `@task` Decorator with Weight Parameter**

```python
from locust import HttpUser, task, between

class WeightedUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(1)  # Weight 1 - least frequent
    def rare_action(self):
        self.client.get("/admin/settings")
    
    @task(3)  # Weight 3 - 3x more likely than rare_action
    def common_action(self):
        self.client.get("/products")
    
    @task(6)  # Weight 6 - 6x more likely than rare_action
    def very_common_action(self):
        self.client.get("/")
```

**Probability calculation:**
- Total weight = 1 + 3 + 6 = 10
- `rare_action`: 1/10 = 10% chance
- `common_action`: 3/10 = 30% chance
- `very_common_action`: 6/10 = 60% chance

#### **Method 2: Using `tasks` List with Tuples**

```python
from locust import HttpUser, task, between

def browse_homepage(user):
    user.client.get("/")

def view_products(user):
    user.client.get("/products")

def checkout(user):
    user.client.post("/checkout")

class TupleWeightedUser(HttpUser):
    wait_time = between(1, 3)
    
    # Format: (task_function, weight)
    tasks = [
        (browse_homepage, 5),   # 5x more likely
        (view_products, 3),     # 3x more likely
        (checkout, 1),          # Least likely
    ]
```

#### **Method 3: Using TaskSet with Weights**

```python
from locust import HttpUser, TaskSet, task, between

class BrowseTasks(TaskSet):
    @task(5)
    def homepage(self):
        self.client.get("/")
    
    @task(3)
    def products(self):
        self.client.get("/products")

class CheckoutTasks(TaskSet):
    @task(1)
    def view_cart(self):
        self.client.get("/cart")
    
    @task(2)
    def complete_purchase(self):
        self.client.post("/checkout")

class WeightedTaskSetUser(HttpUser):
    wait_time = between(1, 3)
    
    # Weight entire TaskSets
    tasks = [
        (BrowseTasks, 8),   # 80% of time browsing
        (CheckoutTasks, 2), # 20% of time checking out
    ]
```

### Real-World Example: E-commerce Site

```python
from locust import HttpUser, task, between

class EcommerceUser(HttpUser):
    """Simulates realistic user behavior with proper weighting"""
    wait_time = between(2, 5)
    
    @task(10)  # Most users just browse
    def browse_products(self):
        self.client.get("/products")
    
    @task(5)  # Some view product details
    def view_product_detail(self):
        product_id = random.randint(1, 100)
        self.client.get(f"/products/{product_id}")
    
    @task(3)  # Fewer add to cart
    def add_to_cart(self):
        product_id = random.randint(1, 100)
        self.client.post("/cart/add", json={"product_id": product_id})
    
    @task(1)  # Even fewer checkout
    def checkout(self):
        self.client.post("/checkout")
    
    @task(0.5)  # Very few contact support
    def contact_support(self):
        self.client.get("/support")
```

---

## 2. Task Sequencing

Task sequencing controls the **order** in which tasks are executed. By default, Locust randomly selects tasks based on weights. Sequencing allows you to enforce a specific order.

### Why Use Sequencing?

- Testing user journeys (login → browse → purchase)
- Ensuring dependencies (must login before accessing protected resources)
- Simulating realistic user flows

### Methods for Task Sequencing

#### **Method 1: Using `on_start` and `on_stop`**

```python
from locust import HttpUser, task, between

class SequentialUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called once when user starts - perfect for setup"""
        # Step 1: Login
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        self.token = response.json().get("token")
        print("User logged in")
    
    @task
    def browse_authenticated(self):
        """Step 2: Browse with authentication"""
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/dashboard", headers=headers)
    
    @task
    def view_profile(self):
        """Step 3: View profile"""
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/profile", headers=headers)
    
    def on_stop(self):
        """Called once when user stops - perfect for cleanup"""
        # Step 4: Logout
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/logout", headers=headers)
        print("User logged out")
```

**Note:** Tasks decorated with `@task` still execute randomly after `on_start`. For strict sequencing, use other methods.

#### **Method 2: Manual Sequencing in a Single Task**

```python
from locust import HttpUser, task, between

class StrictSequenceUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def complete_user_journey(self):
        """Execute tasks in strict order"""
        
        # Step 1: Login
        login_response = self.client.post("/login", json={
            "username": "user",
            "password": "pass"
        })
        assert login_response.status_code == 200
        token = login_response.json().get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 2: Browse products
        browse_response = self.client.get("/products", headers=headers)
        assert browse_response.status_code == 200
        
        # Step 3: View specific product
        product_response = self.client.get("/products/123", headers=headers)
        assert product_response.status_code == 200
        
        # Step 4: Add to cart
        cart_response = self.client.post("/cart/add", 
                                        json={"product_id": 123},
                                        headers=headers)
        assert cart_response.status_code == 200
        
        # Step 5: Checkout
        checkout_response = self.client.post("/checkout", headers=headers)
        assert checkout_response.status_code == 200
```

**Pros:** Simple, guaranteed order
**Cons:** All steps count as one task, harder to track individual step performance

#### **Method 3: Using TaskSet with `@seq_task` (Locust 2.0+)**

```python
from locust import HttpUser, TaskSet, task, seq_task, between

class UserJourney(TaskSet):
    """Defines a sequential user journey"""
    
    @seq_task(1)  # First task in sequence
    def login(self):
        response = self.client.post("/login", json={
            "username": "user",
            "password": "pass"
        })
        self.token = response.json().get("token")
    
    @seq_task(2)  # Second task in sequence
    def browse_products(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/products", headers=headers)
    
    @seq_task(3)  # Third task in sequence
    def view_product(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/products/123", headers=headers)
    
    @seq_task(4)  # Fourth task in sequence
    def add_to_cart(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/cart/add", 
                        json={"product_id": 123},
                        headers=headers)
    
    @seq_task(5)  # Fifth task in sequence
    def checkout(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/checkout", headers=headers)

class SequentialJourneyUser(HttpUser):
    wait_time = between(1, 3)
    tasks = [UserJourney]
```

**Key points:**
- Tasks execute in order: 1 → 2 → 3 → 4 → 5
- After completing the sequence, it starts over from 1
- Each step is tracked separately in statistics

#### **Method 4: Combining Weighting and Sequencing**

```python
from locust import HttpUser, TaskSet, task, seq_task, between
import random

class BrowseOnly(TaskSet):
    """Users who just browse (no purchase)"""
    
    @seq_task(1)
    def login(self):
        response = self.client.post("/login", json={
            "username": "browser",
            "password": "pass"
        })
        self.token = response.json().get("token")
    
    @seq_task(2)
    def browse(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/products", headers=headers)
    
    @seq_task(3)
    def logout(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/logout", headers=headers)

class FullPurchaseJourney(TaskSet):
    """Users who complete a purchase"""
    
    @seq_task(1)
    def login(self):
        response = self.client.post("/login", json={
            "username": "buyer",
            "password": "pass"
        })
        self.token = response.json().get("token")
    
    @seq_task(2)
    def browse(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/products", headers=headers)
    
    @seq_task(3)
    def purchase(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/checkout", headers=headers)
    
    @seq_task(4)
    def logout(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/logout", headers=headers)

class MixedBehaviorUser(HttpUser):
    wait_time = between(1, 3)
    
    # 70% browse only, 30% full purchase
    tasks = [
        (BrowseOnly, 7),
        (FullPurchaseJourney, 3),
    ]
```

---

## Comparison Table

| Feature | Task Weighting | Task Sequencing |
|---------|---------------|-----------------|
| **Purpose** | Control frequency/probability | Control execution order |
| **Default behavior** | Equal probability | Random selection |
| **Use case** | Realistic traffic distribution | User journeys/workflows |
| **Implementation** | `@task(weight)` or tuples | `@seq_task()`, `on_start`, manual |
| **Flexibility** | High (probabilistic) | Strict (deterministic) |
| **Tracking** | Each task tracked separately | Depends on method used |
| **Best for** | Load testing general usage | Testing specific workflows |

---

## Best Practices

### For Weighting:
1. **Analyze real traffic patterns** to set accurate weights
2. **Start with simple ratios** (1:2:3) and adjust based on data
3. **Document your weights** so team understands the simulation
4. **Review and update** weights as application usage changes

### For Sequencing:
1. **Use `@seq_task`** for clear, maintainable sequences
2. **Handle failures gracefully** - don't let one failed step break the whole flow
3. **Use `on_start`** for setup (login, initialization)
4. **Use `on_stop`** for cleanup (logout, resource release)
5. **Combine with weighting** for realistic mixed behavior

### Combined Approach (Recommended):

```python
from locust import HttpUser, TaskSet, task, seq_task, between

class AuthenticatedBrowsing(TaskSet):
    """Weighted tasks within a sequential context"""
    
    def on_start(self):
        # Sequence: Always login first
        response = self.client.post("/login", json={
            "username": "user",
            "password": "pass"
        })
        self.token = response.json().get("token")
    
    @task(5)  # Weighted: Browse more often
    def browse_products(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/products", headers=headers)
    
    @task(2)  # Weighted: View details less often
    def view_details(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/products/123", headers=headers)
    
    @task(1)  # Weighted: Checkout least often
    def checkout(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/checkout", headers=headers)
    
    def on_stop(self):
        # Sequence: Always logout at end
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/logout", headers=headers)

class RealisticUser(HttpUser):
    wait_time = between(1, 3)
    tasks = [AuthenticatedBrowsing]
```

This gives you:
- ✅ **Sequencing**: Login → Tasks → Logout
- ✅ **Weighting**: Different task frequencies within the session
- ✅ **Realism**: Mimics actual user behavior patterns