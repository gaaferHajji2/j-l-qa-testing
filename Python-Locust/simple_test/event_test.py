from locust import events, task, HttpUser

@events.test_start.add_listener
def on_start_test(environment, **kwargs):
    print("The test has begin")

@events.test_stop.add_listener
def on_stop_test(environment, **kwargs):
    print("The test has been finished")
class SimpleEvent(HttpUser):
    @task(3)
    def task_01(self):
        self.client.get('/')

    @task
    def task_02(self):
        self.client.post('/')