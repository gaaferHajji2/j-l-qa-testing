from locust import task, FastHttpUser

class Test01(FastHttpUser):
    host= 'https://locust.io'
    # wait_time = between(1, 2)

    @task
    def check_request(self):
        # We must define the response variable
        response = self.client.get('/')