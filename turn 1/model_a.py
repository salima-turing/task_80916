import time
from locust import HttpUser, TaskSet, task, between
from faker import Faker

fake = Faker()

class UserBehavior(TaskSet):

	@task
	def login_logout(self):
		username = fake.user_name()
		password = fake.password()

		# Login
		response = self.client.post("/login", json={"username": username, "password": password})
		assert response.status_code == 200

		# Perform some actions as a logged-in user
		self.client.get("/dashboard")
		time.sleep(2)

		# Logout
		response = self.client.post("/logout")
		assert response.status_code == 200

	@task
	def view_product_page(self):
		product_id = fake.random_int(min=1, max=1000)
		self.client.get(f"/products/{product_id}")

class WebsiteUser(HttpUser):
	tasks = [UserBehavior]
	wait_time = between(5, 15)

if __name__ == "__main__":
	import os
	os.system("locust -f test_locust.py --host=http://your_web_portal_url")
