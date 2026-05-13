from locust import LoadTestShape
from simple_test_01 import UserA, UserB

class StagesShapeWithCustomUsers(LoadTestShape):
    time_limit = 60 # 1-minutes
    spawn_rate = 50
    use_common_options = True

    stages = [
        {"duration": 10, "users": 10, "spawn_rate": 10, "user_classes": [UserA]},
        {"duration": 30, "users": 50, "spawn_rate": 10, "user_classes": [UserA, UserB]},
        {"duration": 60, "users": 100, "spawn_rate": 10, "user_classes": [UserB]},
        {"duration": 120, "users": 100, "spawn_rate": 10, "user_classes": [UserA,UserB]},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            # if run_time < self.runner.environment.parsed_options.run_time:
            if run_time < stage["duration"]:
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                    print('Success-01')
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                    print('Failure-01')
                return tick_data

        return None
