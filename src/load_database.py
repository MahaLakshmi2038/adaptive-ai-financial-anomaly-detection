import pandas as pd
from database import get_connection

RESULTS_FILE = "results/anomaly_results.csv"


# Load ML results
df = pd.read_csv(RESULTS_FILE)

conn = get_connection()
cursor = conn.cursor()

# Insert transactions into database
for _, row in df.iterrows():

    cursor.execute("""
        INSERT OR REPLACE INTO transactions
        (transaction_id, amount, merchant_category,
         risk_score, risk_level, anomaly)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        row["Transaction_ID"],
        row["Amount"],
        row["Merchant_Category"],
        row["Risk_Score"],
        row["Risk_Level"],
        row["Anomaly"]
    ))

conn.commit()

# Check number of records
cursor.execute("SELECT COUNT(*) FROM transactions")

count = cursor.fetchone()[0]

conn.close()

print("Transactions loaded into SQLite:", count)