from locust import HttpUser, TaskSet, task, between
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Define the User Behavior Scenario using Selenium
class PortalUserBehavior(TaskSet):
    def on_start(self):
        # Initialize a Chrome web driver
        self.driver = webdriver.Chrome(service=ChromeService(executable_path="path_to_chromedriver.exe"))
        self.driver.get("http://your_python_web_portal_url")

    def login(self):
        username_field = self.driver.find_element(By.ID, "username")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login_button")

        username_field.send_keys("dummy_user")
        password_field.send_keys("dummy_password")
        login_button.click()

        # Wait for the page to load after login
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard_heading")))

    def navigate_to_dashboard(self):
        dashboard_link = self.driver.find_element(By.LINK_TEXT, "Dashboard")
        dashboard_link.click()

    def view_product_details(self):
        product_link = self.driver.find_element(By.LINK_TEXT, "Product X")
        product_link.click()
        # Add more actions for viewing product details

    @task
    def user_flow(self):
        self.login()
        self.navigate_to_dashboard()
        self.view_product_details()
        # Add more tasks for different user actions

    def on_stop(self):
        self.driver.quit()

# Step 2: Define the Locust Test Class
class WebsiteUser(HttpUser):
    host = "http://your_python_web_portal_url"  # This is used by Locust for reporting, but we won't be making HTTP requests directly.
    wait_time = between(5, 15)  # Think time between user actions

    tasks = [PortalUserBehavior]

if __name__ == "__main__":
    WebsiteUser().run()
