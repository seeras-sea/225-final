import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

class TestHtmlElements(unittest.TestCase):
    
    def setUp(self):
        # Set up headless Firefox browser
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        # Use the service IP address for the Flask app
        self.driver.get("http://flask-dev-service:5000")
    
    def test_page_title(self):
        # Check if the page title is correct
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