from app import init_db
import sqlite3
#Function to add referees column to the database.
def add_referees_column():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE resumes ADD COLUMN referees TEXT')
        conn.commit()
    except sqlite3.OperationalError:
        #  Checks if Column might already exist
        pass
    conn.close()

if __name__ == '__main__':
    init_db()
    add_referees_column()
    print("Migration completed successfully!") 