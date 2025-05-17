import sqlite3
import random
import os

DATABASE = '/nfs/app.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def generate_test_data():
    db = get_db()
    
    # Sample data
    names = ['John Smith', 'Jane Doe', 'Robert Johnson', 'Emily Davis', 'Michael Brown', 
             'Sarah Wilson', 'David Miller', 'Lisa Moore', 'James Taylor', 'Jennifer Anderson']
    
    # Generate phone numbers and emails
    for name in names:
        phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        email = f"{name.lower().replace(' ', '.')}@example.com"
        
        # Insert into database
        db.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', 
                  (name, phone, email))
    
    db.commit()
    print(f"Generated {len(names)} test contacts")

if __name__ == '__main__':
    generate_test_data()