import time
from locust import HttpUser, task, between, TaskSet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PortalUserBehavior(TaskSet):
	def on_start(self):
		self.driver = webdriver.Chrome(service=ChromeService (executable_path='/path/to/chromedriver'))
		self.driver.get("http://your_python_web_portal_url")

	@task
	def user_flow(self):
		self.login()
		self.navigate_to_dashboard()
		self.view_product_details()

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
		time.sleep(2) # Add a delay if needed for page loading

	def on_stop(self):
		self.driver.quit()


class WebsiteUser(HttpUser):
	tasks = [PortalUserBehavior]
	wait_time = between(5, 15)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client = None

if __name__ == "__main__":
	WebsiteUser().run()
