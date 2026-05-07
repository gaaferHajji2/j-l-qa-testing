from locust import LoadTestShape

class MyLoadTestShape(LoadTestShape):
    # time_limit = 600 # 10-minutes
    time_limit = 60 # 1-minutes
    spawn_rate = 20

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.time_limit:
            # User count rounded to nearest hundred.
            user_count = round(run_time, -2)
            print(f'The user count: {user_count} & spawn rate: {self.spawn_rate}')
            return (user_count, self.spawn_rate)

        return None
