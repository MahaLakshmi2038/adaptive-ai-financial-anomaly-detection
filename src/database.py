import sqlite3

DB_FILE = "results/financial_anomaly.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Store detected transactions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE,
            amount REAL,
            merchant_category TEXT,
            risk_score REAL,
            risk_level TEXT,
            anomaly INTEGER
        )
    """)

    # Store administrator feedback
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            admin_label TEXT
        )
    """)

    # Store adaptive configuration
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adaptive_config (
            id INTEGER PRIMARY KEY,
            risk_threshold REAL
        )
    """)

    # Set initial adaptive threshold
    cursor.execute("""
        INSERT OR IGNORE INTO adaptive_config
        (id, risk_threshold)
        VALUES (1, 40)
    """)

    conn.commit()
    conn.close()

    print("SQLite database initialized successfully.")


if __name__ == "__main__":
    initialize_database()