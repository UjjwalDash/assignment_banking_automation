import sqlite3
import random

def create_database():
    conn = sqlite3.connect(r"C:\Users\dashu\Desktop\personal_projects\automate_banking_dispute\app\database\sql_db\transactions.db")
    cursor = conn.cursor()

    # Create transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert sample transactions
    users = list(range(1, 21))  # 20 users
    for _ in range(50):  # More than 20 transactions
        user_id = random.choice(users)
        amount = round(random.uniform(10, 500), 2)
        cursor.execute("INSERT INTO transactions (user_id, amount) VALUES (?, ?)", (user_id, amount))

    conn.commit()
    conn.close()
    print("Database created with sample transactions.")

if __name__ == "__main__":
    create_database()
