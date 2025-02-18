from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    host = "http://0.0.0.0:8000"
    wait_time = between(1, 5)  # 模擬用戶等待時間

    @task
    def post_task(self):
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "title": "Testing Task",
            "description": "Testing description",
        }
        self.client.post("/tasks", json=data, headers=headers)