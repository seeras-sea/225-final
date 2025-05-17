import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
import os
import time
import socket

class TestHtmlElements(unittest.TestCase):
    
    def setUp(self):
        # Set up headless Firefox browser
        options = Options()
        options.add_argument("--headless")
        
        # Add more Firefox options to improve stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the driver
        self.driver = webdriver.Firefox(options=options)
        self.driver.set_page_load_timeout(30)  # Set page load timeout
        
        # Get the Flask app URL from environment variable or use the specified IP
        flask_url = os.environ.get('FLASK_URL', 'http://10.48.10.170')
        print("Connecting to Flask app at:", flask_url)
        
        # Try to resolve the hostname first if it's not an IP address
        if not self._is_ip_address(flask_url.split('//')[1].split(':')[0]):
            self._check_dns_resolution(flask_url)
        
        # Try to connect to the Flask app with retries
        max_retries = 2  
        for attempt in range(max_retries):
            try:
                self.driver.get(flask_url)
                print("Successfully connected to", flask_url)
                
                # Wait for the page to be fully loaded
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print("Page fully loaded")
                break
            except (WebDriverException, TimeoutException) as e:
                if attempt < max_retries - 1:
                    print("Connection attempt", attempt + 1, "failed:", str(e))
                    print("Retrying in 10 seconds...")  # Increase wait time
                    time.sleep(10)
                else:
                    print("All", max_retries, "connection attempts failed")
                    raise e
    
    def _is_ip_address(self, host):
        """Check if the host is an IP address."""
        try:
            socket.inet_aton(host)
            return True
        except socket.error:
            return False
    
    def _check_dns_resolution(self, url):
        """Check if the hostname in the URL can be resolved."""
        hostname = url.split('//')[1].split(':')[0]
        try:
            print("Resolving hostname:", hostname)
            ip = socket.gethostbyname(hostname)
            print("Hostname", hostname, "resolved to", ip)
        except socket.gaierror as e:
            print("DNS resolution failed for", hostname, ":", str(e))
            print("Attempting to use /etc/hosts or equivalent...")
    
    def test_page_title(self):
        # Check if the page title is correct
        try:
            print("Page title:", self.driver.title)
            self.assertEqual("Contact Manager", self.driver.title)
        except AssertionError as e:
            print("Error in test_page_title:", str(e))
            # Take screenshot for debugging
            self.driver.save_screenshot('title_test_error.png')
            raise
    
    def test_form_exists(self):
        try:
            # Wait for form to be present
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            self.assertIsNotNone(form)
            
            # Wait for inputs to be present
            name_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "name"))
            )
            phone_input = self.driver.find_element(By.NAME, "phone")
            email_input = self.driver.find_element(By.NAME, "email")
            
            self.assertIsNotNone(name_input)
            self.assertIsNotNone(phone_input)
            self.assertIsNotNone(email_input)
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            print("Error in test_form_exists:", str(e))
            # Take screenshot for debugging
            self.driver.save_screenshot('form_test_error.png')
            raise
    
    def test_table_exists(self):
        try:
            # Wait for table to be present
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            self.assertIsNotNone(table)
            
            # Wait for headers to be present
            headers = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "th"))
            )
            self.assertEqual(len(headers), 5)  # ID, Name, Phone, Email, Action
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            print("Error in test_table_exists:", str(e))
            # Take screenshot for debugging
            self.driver.save_screenshot('table_test_error.png')
            raise
    
    def tearDown(self):
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except WebDriverException as e:
                print("Error in tearDown:", str(e))

if __name__ == "__main__":
    unittest.main()
