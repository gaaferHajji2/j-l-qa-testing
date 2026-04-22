from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get('/hello')
    @task
    def hello_world_02(self):
        self.client.get('/world')