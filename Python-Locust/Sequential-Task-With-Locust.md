### 1. Latest Version of Locust
As of **August 2026**, the Locust project is actively maintained and is in the **2.3x / 2.4x release series** (e.g., `2.34.x` or newer). Locust follows a rapid release cycle, so minor patches and features are added frequently. 

To check the absolute latest version available on PyPI right now and install/upgrade it, you can run:
```bash
pip install --upgrade locust
# Or to see the latest version available without installing:
pip index versions locust
```

---

### 2. How to Perform Sequential Testing in Locust
By default, if you define multiple `@task` methods in a standard `User` or `TaskSet` class, Locust will pick them **randomly** based on their assigned weights. 

If you need to simulate a strict user journey (e.g., *Login -> View Dashboard -> Logout*), you have two primary ways to enforce sequential execution:

#### Method A: Use `SequentialTaskSet` (Recommended for modular flows)
Locust provides a built-in class called `SequentialTaskSet`. Tasks decorated with `@task` inside this class will be executed in the **exact order they are defined**. 

Once the last task is executed, the sequence will loop back to the first task unless you explicitly tell it to stop using `self.interrupt()`.

```python
from locust import User, task, SequentialTaskSet, between

class SequentialUserFlow(SequentialTaskSet):
    
    @task
    def step_1_login(self):
        with self.client.post("/login", json={"user": "test", "pass": "123"}, catch_response=True) as response:
            if response.status_code == 200:
                # Save state to use in the next sequential step
                self.token = response.json().get("token") 
                response.success()
            else:
                response.failure("Login failed")

    @task
    def step_2_view_dashboard(self):
        # Use the token from the previous step
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/dashboard", headers=headers)

    @task
    def step_3_logout(self):
        self.client.post("/logout")
        # interrupt() stops the sequence and returns control to the User class.
        # Without this, the sequence would loop back to step_1_login.
        self.interrupt() 

class MyWebsiteUser(User):
    wait_time = between(1, 3)
    tasks = [SequentialUserFlow]
```

#### Method B: Use a Single `@task` Method (Recommended for simple, linear scripts)
If your sequential flow doesn't require complex modularity or branching, the simplest approach is to just write all your sequential steps inside a **single** `@task` method. Locust will execute the Python code from top to bottom.

```python
from locust import User, task, between

class SimpleSequentialUser(User):
    wait_time = between(1, 2)

    @task
    def complete_user_journey(self):
        # Step 1
        self.client.get("/")
        
        # Step 2
        self.client.get("/products")
        
        # Step 3
        self.client.post("/cart/add", json={"item_id": 123})
        
        # Step 4
        self.client.post("/checkout")
```

### 💡 Pro-Tips for Sequential Testing
1. **Sharing Data Between Steps:** If you use `SequentialTaskSet`, you can easily pass data between steps by attaching variables to the `TaskSet` instance (e.g., `self.order_id = ...` in step 1, and `self.client.get(f"/orders/{self.order_id}")` in step 2).
2. **Failing Fast:** If a critical early step fails (like a Login), you usually don't want to continue the sequence. You can use `self.interrupt(reschedule=True)` or raise an exception to abort the sequence and immediately start a new iteration/user.
3. **Think Time:** Don't forget to use `self.wait_time()` or `gevent.sleep()` between heavy sequential steps if you want to accurately mimic human reading/thinking time between clicks.