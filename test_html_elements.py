import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import time

class TestHtmlElements(unittest.TestCase):
    
    def setUp(self):
        # Set up headless Firefox browser
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        
        # Get the Flask app URL from environment variable or use default
        flask_url = os.environ.get('FLASK_URL', 'http://flask-dev-service:5000')
        print(f"Connecting to Flask app at: {flask_url}")
        
        # Try to connect to the Flask app with retries
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.driver.get(flask_url)
                print(f"Successfully connected to {flask_url}")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Connection attempt {attempt+1} failed: {str(e)}")
                    print(f"Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"All {max_retries} connection attempts failed")
                    raise e
    
    def test_page_title(self):
        # Check if the page title is correct
        print(f"Page title: {self.driver.title}")
        self.assertEqual("Contact Manager", self.driver.title)
    
    def test_form_exists(self):
        # Check if the form exists
        form = self.driver.find_element(By.TAG_NAME, "form")
        self.assertIsNotNone(form)
        
        # Check if form inputs exist
        name_input = self.driver.find_element(By.NAME, "name")
        phone_input = self.driver.find_element(By.NAME, "phone")
        email_input = self.driver.find_element(By.NAME, "email")
        
        self.assertIsNotNone(name_input)
        self.assertIsNotNone(phone_input)
        self.assertIsNotNone(email_input)
    
    def test_table_exists(self):
        # Check if the table exists
        table = self.driver.find_element(By.TAG_NAME, "table")
        self.assertIsNotNone(table)
        
        # Check if table headers exist
        headers = self.driver.find_elements(By.TAG_NAME, "th")
        self.assertEqual(len(headers), 5)  # ID, Name, Phone, Email, Action
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
