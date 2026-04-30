from locust import task, HttpUser
import locust.stats

from math import floor, log10

def my_bucket_function(response_time: int | float) -> int:
    """Example: bucket to 3 significant figures."""
    if response_time == 0:
        return 0
    return int(round(response_time, -int(floor(log10(abs(response_time)))) + 2))

locust.stats.bucket_response_time = my_bucket_function

class TestStats(HttpUser):
    @task
    def get_index(self):
        self.client.get('/posts')

    @task
    def get_about(self):
        self.client.get('/todos')
    
    @task
    def get_contact(self):
        self.client.get('/users')