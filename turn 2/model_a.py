from locust import HttpUser, TaskSet, task, between
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest.mock import patch
import requests

# Step 1: Define the User Behavior Scenario using Selenium
class PortalUserBehavior(TaskSet):

	def on_start(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		self.driver = webdriver.Chrome(options=options)
		self.driver.get("http://your_python_web_portal_url")

	def login(self):
		username_field = self.driver.find_element(By.ID, "username")
		password_field = self.driver.find_element(By.ID, "password")
		login_button = self.driver.find_element(By.ID, "login_button")

		username_field.send_keys("dummy_user")
		password_field.send_keys("dummy_password")
		login_button.click()

		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard_heading")))

	def navigate_to_dashboard(self):
		dashboard_link = self.driver.find_element(By.LINK_TEXT, "Dashboard")
		dashboard_link.click()

	def view_product_details(self):
		product_link = self.driver.find_element(By.LINK_TEXT, "Product X")
		product_link.click()

	@task
	def user_flow(self):
		self.login()
		self.navigate_to_dashboard()
		self.view_product_details()

	def on_stop(self):
		self.driver.quit()


# Step 2: Define the Locust Test Class
class WebsiteUser(HttpUser):
	host = "http://your_python_web_portal_url"
	wait_time = between(1, 5)

	tasks = [PortalUserBehavior]


if __name__ == "__main__":
	import os
	if "CI" in os.environ:
		# Mocking external service requests during CI
		with patch('requests.get') as mock_get:
			mock_get.return_value.status_code = 200
			mock_get.return_value.text = '{"key": "value"}'
			WebsiteUser().run()
	else:
		WebsiteUser().run()
