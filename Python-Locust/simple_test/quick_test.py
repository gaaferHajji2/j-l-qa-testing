import time
from locust import HttpUser, task, between

class QuickStartUser(HttpUser):
    wait_time = between(1, 10)

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    # maximize the chance to choose this task by 3-times
    @task(3)
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
            time.sleep(1)

    def on_start(self):
        self.client.post("/login", json={"username":"foo", "password":"bar"})
