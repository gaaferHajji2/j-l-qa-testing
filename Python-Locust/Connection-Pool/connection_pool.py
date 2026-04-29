from locust import HttpUser, task
from urllib3 import PoolManager

class TestConnectionPool(HttpUser):
    pool_manager = PoolManager(maxsize=100, block=True)
    @task
    def get_hello_world(self):
        self.client.get('/')