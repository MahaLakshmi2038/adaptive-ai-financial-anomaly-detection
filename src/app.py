from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_connection

app = FastAPI(
    title="Adaptive Financial Anomaly Detection API",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Adaptive Financial Anomaly Detection API is running"
    }


@app.get("/transactions")
def get_transactions(limit: int = 20):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT transaction_id, amount, merchant_category,
               risk_score, risk_level, anomaly
        FROM transactions
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "transaction_id": row[0],
            "amount": row[1],
            "merchant_category": row[2],
            "risk_score": row[3],
            "risk_level": row[4],
            "anomaly": row[5]
        }
        for row in rows
    ]


@app.get("/anomalies")
def get_anomalies():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT transaction_id, amount, merchant_category,
               risk_score, risk_level
        FROM transactions
        WHERE anomaly = 1
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "transaction_id": row[0],
            "amount": row[1],
            "merchant_category": row[2],
            "risk_score": row[3],
            "risk_level": row[4]
        }
        for row in rows
    ]


@app.get("/summary")
def get_summary():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE anomaly = 1"
    )
    anomalies = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE risk_level = 'Normal'"
    )
    normal = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE risk_level = 'Suspicious'"
    )
    suspicious = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE risk_level = 'High Risk'"
    )
    high_risk = cursor.fetchone()[0]

    conn.close()

    return {
        "total_transactions": total,
        "anomalies": anomalies,
        "normal": normal,
        "suspicious": suspicious,
        "high_risk": high_risk
    }


@app.post("/feedback")
def add_feedback(transaction_id: str, admin_label: str):

    conn = get_connection()
    cursor = conn.cursor()

    # Store administrator feedback
    cursor.execute("""
        INSERT INTO feedback
        (transaction_id, admin_label)
        VALUES (?, ?)
    """, (transaction_id, admin_label))

    # Count feedback
    cursor.execute("""
        SELECT COUNT(*)
        FROM feedback
        WHERE admin_label = 'False Positive'
    """)

    false_positives = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM feedback
        WHERE admin_label = 'Genuine Anomaly'
    """)

    genuine_anomalies = cursor.fetchone()[0]

    total_feedback = false_positives + genuine_anomalies

    # Current threshold
    base_threshold = 40

    # Adaptive threshold
    if total_feedback > 0:

        false_positive_rate = (
            false_positives / total_feedback
        )

        if false_positive_rate > 0.30:
            new_threshold = base_threshold + 5

        elif false_positive_rate < 0.10:
            new_threshold = base_threshold - 5

        else:
            new_threshold = base_threshold

    else:
        new_threshold = base_threshold

    # Save updated threshold
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adaptive_config (
            id INTEGER PRIMARY KEY,
            risk_threshold REAL
        )
    """)

    cursor.execute("""
        INSERT OR REPLACE INTO adaptive_config
        (id, risk_threshold)
        VALUES (1, ?)
    """, (new_threshold,))

    conn.commit()
    conn.close()

    return {
        "message": "Feedback recorded and system adapted",
        "transaction_id": transaction_id,
        "admin_label": admin_label,
        "new_risk_threshold": new_threshold
    }

@app.get("/adaptive-status")
def adaptive_status():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT risk_threshold
        FROM adaptive_config
        WHERE id = 1
    """)

    result = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*)
        FROM feedback
    """)

    feedback_count = cursor.fetchone()[0]

    conn.close()

    return {
        "risk_threshold": result[0] if result else 40,
        "feedback_count": feedback_count
    }
@app.post("/analyze")
def analyze_transaction(
    amount: float,
    distance_from_home: float,
    ip_risk_score: float,
    avg_spending_habit: float,
    is_weekend: int,
    is_night_transaction: int
):
    # Simple behavioral risk calculation
    risk_score = 0

    if amount > avg_spending_habit * 2:
        risk_score += 30

    if distance_from_home > 50:
        risk_score += 20

    if ip_risk_score > 70:
        risk_score += 25

    if is_weekend == 1:
        risk_score += 10

    if is_night_transaction == 1:
        risk_score += 15

    if risk_score >= 60:
        risk_level = "High Risk"
    elif risk_score >= 40:
        risk_level = "Suspicious"
    else:
        risk_level = "Normal"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }