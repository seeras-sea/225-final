import sqlite3

DATABASE = '/nfs/app.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def clear_test_data():
    db = get_db()
    
    # Delete all records from the contacts table
    db.execute('DELETE FROM contacts')
    db.commit()
    
    print("All test data has been cleared from the database")

if __name__ == '__main__':
    clear_test_data()
