from locust import events, task, HttpUser
from locust.runners import MasterRunner

@events.test_start.add_listener
def on_start_test(environment, **kwargs):
    print("The test has begin")

@events.test_stop.add_listener
def on_stop_test(environment, **kwargs):
    print("The test has been finished")

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("I'm on master node")
    else:
        print("I'm on a worker or standalone node")

class SimpleEvent(HttpUser):
    @task(3)
    def task_01(self):
        response = self.client.get('/')
        print(f"Task 1 response status code: {response.status_code}")
        print(f"The response text of Task 1: {response.text}")

    @task
    def task_02(self):
        response = self.client.post('/')
        print(f"Task 2 response status code: {response.status_code}")
        print(f"The response text of Task 2: {response.text}")