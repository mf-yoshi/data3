from locust import HttpUser, TaskSet, task, between, constant, constant_pacing, User
from locust.contrib.fasthttp import FastHttpUser

class QuickstartUser(HttpUser):
    wait_time = constant_pacing(1)

    @task(1)
    def search(self):
        self.client.get("/", verify=False)
