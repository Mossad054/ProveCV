import sqlite3

def init_database():
    # Connects to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('resumes.db')
    print("Connected to database successfully")

    try:
        # Creates a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Creates users table id if doesn't exist.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        ''')

        # Commit the changes to the database.
        conn.commit()
        print("Users table created successfully")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Closes datbase the connection
        conn.close()
        print("Database connection closed")

if __name__ == "__main__":
    init_database() 