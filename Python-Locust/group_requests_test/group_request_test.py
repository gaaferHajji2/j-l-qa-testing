from locust import HttpUser, task

class HomePage(HttpUser):
    @task
    def hello_01(self):
        for _ in range(10):
            self.client.get('/', name='JLoka-[id]')

    @task
    def hello_02(self):
        self.client.request_name = 'JLoka-02-[id]'
        for _ in range(10):
            self.client.get('/about')
        self.client.request_name = None