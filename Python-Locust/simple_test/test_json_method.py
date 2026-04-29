from locust import task, HttpUser

class Example01(HttpUser):
    @task
    def get_data(self):
        self.client.get("/")
    
    @classmethod
    def json(cls):
        return {
            "host": cls.host,
            "arg-01": "JLoka-01"
        }