from locust import task, FastHttpUser, between

class Test01(FastHttpUser):
    host= 'https://locust.io'
    wait_time = between(0.1, 1)

    @task
    def check_request(self):
        self.client.get('/')