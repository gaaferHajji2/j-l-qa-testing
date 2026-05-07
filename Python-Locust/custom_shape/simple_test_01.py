from locust import task, HttpUser

class MySimpleTest(HttpUser):
    @task
    def simple_task_01(self):
        self.client.get('/')