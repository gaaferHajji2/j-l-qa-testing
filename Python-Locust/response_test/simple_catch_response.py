from locust import HttpUser, task

class HomePage(HttpUser):
    @task
    def hello_01(self):
        with self.client.get('/', catch_response=True) as response:
            if response.elapsed.total_seconds()> 3:
                response.failure("Too Long Time: Task-01")
    @task
    def hello_02(self):
        with self.client.get('/about', catch_response=True) as response:
            if response.elapsed.total_seconds() > 3:
                response.failure("Too Long Time: Task:-02")
            elif response.status_code == 404:
                response.success()