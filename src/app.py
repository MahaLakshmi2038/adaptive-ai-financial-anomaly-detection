from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_connection

import pandas as pd
import os


app = FastAPI(
    title="Adaptive Financial Anomaly Detection API",
    version="2.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ADAPTIVE_CONFIG_FILE = "results/adaptive_config.csv"
BASE_THRESHOLD = 40


# ============================================================
# HELPER — SAVE ADAPTIVE CONFIGURATION
# ============================================================

def save_adaptive_config(threshold):

    config = pd.DataFrame({
        "Parameter": ["Risk_Threshold"],
        "Value": [threshold]
    })

    config.to_csv(
        ADAPTIVE_CONFIG_FILE,
        index=False
    )


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message":
        "Adaptive Financial Anomaly Detection API is running"
    }


# ============================================================
# TRANSACTIONS
# ============================================================

@app.get("/transactions")
def get_transactions(limit: int = 20):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT transaction_id,
               amount,
               merchant_category,
               risk_score,
               risk_level,
               anomaly
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


# ============================================================
# ANOMALIES
# ============================================================

@app.get("/anomalies")
def get_anomalies():

    results_file = "results/anomaly_results.csv"

    if not os.path.exists(results_file):
        return []

    df = pd.read_csv(results_file)

    anomalies = df[df["Anomaly"] == 1].copy()

    return [
        {
            "transaction_id": row["Transaction_ID"],
            "amount": row["Amount"],
            "merchant_category": row["Merchant_Category"],
            "risk_score": row["Risk_Score"],
            "risk_level": row["Risk_Level"],
            "risk_explanation": row.get(
                "Risk_Explanation",
                "Anomaly detected by the risk engine"
            ),
            "drift_status": row.get(
                "Drift_Status",
                "Stable"
            ),
            "historical_anomaly_rate": row.get(
                "Historical_Anomaly_Rate",
                0
            ),
            "recent_anomaly_rate": row.get(
                "Recent_Anomaly_Rate",
                0
            )
        }
        for _, row in anomalies.iterrows()
    ]

# ============================================================
# SUMMARY
# ============================================================

@app.get("/summary")
def get_summary():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions "
        "WHERE anomaly = 1"
    )

    anomalies = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions "
        "WHERE risk_level = 'Normal'"
    )

    normal = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions "
        "WHERE risk_level = 'Suspicious'"
    )

    suspicious = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions "
        "WHERE risk_level = 'High Risk'"
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


# ============================================================
# ADMINISTRATOR FEEDBACK
# ============================================================

@app.post("/feedback")
def add_feedback(
    transaction_id: str,
    admin_label: str
):

    allowed_labels = [
        "Genuine Anomaly",
        "False Positive"
    ]

    if admin_label not in allowed_labels:

        return {
            "error":
            "Invalid admin label. "
            "Use 'Genuine Anomaly' "
            "or 'False Positive'."
        }


    conn = get_connection()
    cursor = conn.cursor()


    # --------------------------------------------------------
    # STORE FEEDBACK
    # --------------------------------------------------------

    cursor.execute("""
        INSERT INTO feedback
        (transaction_id, admin_label)
        VALUES (?, ?)
    """, (
        transaction_id,
        admin_label
    ))


    # --------------------------------------------------------
    # COUNT FEEDBACK
    # --------------------------------------------------------

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


    total_feedback = (
        false_positives
        + genuine_anomalies
    )


    # --------------------------------------------------------
    # ADAPTIVE THRESHOLD
    # --------------------------------------------------------

    if total_feedback > 0:

        false_positive_rate = (
            false_positives
            / total_feedback
        )

        if false_positive_rate > 0.30:

            new_threshold = BASE_THRESHOLD + 5

        elif false_positive_rate < 0.10:

            new_threshold = BASE_THRESHOLD - 5

        else:

            new_threshold = BASE_THRESHOLD

    else:

        new_threshold = BASE_THRESHOLD


    # Keep threshold within safe range

    new_threshold = max(
        30,
        min(new_threshold, 60)
    )


    # --------------------------------------------------------
    # SAVE TO DATABASE
    # --------------------------------------------------------

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
    """, (
        new_threshold,
    ))


    conn.commit()
    conn.close()


    # --------------------------------------------------------
    # KEEP CSV SYNCHRONIZED
    # --------------------------------------------------------

    save_adaptive_config(
        new_threshold
    )


    return {

        "message":
        "Feedback recorded and system adapted",

        "transaction_id":
        transaction_id,

        "admin_label":
        admin_label,

        "false_positive_rate":
        round(
            (
                false_positives
                / total_feedback
            ) * 100,
            2
        )
        if total_feedback > 0
        else 0,

        "new_risk_threshold":
        new_threshold
    }


# ============================================================
# ADAPTIVE STATUS
# ============================================================

@app.get("/adaptive-status")
def adaptive_status():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adaptive_config (
            id INTEGER PRIMARY KEY,
            risk_threshold REAL
        )
    """)


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


    conn.close()


    threshold = (
        result[0]
        if result
        else BASE_THRESHOLD
    )


    total_feedback = (
        false_positives
        + genuine_anomalies
    )


    false_positive_rate = (

        false_positives
        / total_feedback

    ) * 100 if total_feedback > 0 else 0


    return {

        "risk_threshold":
        threshold,

        "feedback_count":
        feedback_count,

        "genuine_anomalies":
        genuine_anomalies,

        "false_positives":
        false_positives,

        "false_positive_rate":
        round(
            false_positive_rate,
            2
        )
    }


# ============================================================
# BEHAVIORAL TRANSACTION ANALYSIS
# ============================================================

@app.post("/analyze")
def analyze_transaction(
    amount: float,
    distance_from_home: float,
    ip_risk_score: float,
    avg_spending_habit: float,
    is_weekend: int,
    is_night_transaction: int
):

    # --------------------------------------------------------
    # CURRENT ADAPTIVE THRESHOLD
    # --------------------------------------------------------

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adaptive_config (
            id INTEGER PRIMARY KEY,
            risk_threshold REAL
        )
    """)


    cursor.execute("""
        SELECT risk_threshold
        FROM adaptive_config
        WHERE id = 1
    """)


    result = cursor.fetchone()

    conn.close()


    adaptive_threshold = (
        result[0]
        if result
        else BASE_THRESHOLD
    )


    # --------------------------------------------------------
    # BEHAVIORAL RISK
    # --------------------------------------------------------

    risk_score = 0

    reasons = []


    if amount > avg_spending_habit * 2:

        risk_score += 30

        reasons.append(
            "Unusual spending amount"
        )


    if distance_from_home > 50:

        risk_score += 20

        reasons.append(
            "Unusual transaction distance"
        )


    if ip_risk_score > 70:

        risk_score += 25

        reasons.append(
            "High-risk IP address"
        )


    if is_weekend == 1:

        risk_score += 10

        reasons.append(
            "Weekend transaction"
        )


    if is_night_transaction == 1:

        risk_score += 15

        reasons.append(
            "Night-time transaction"
        )


    # --------------------------------------------------------
    # ADAPTIVE CLASSIFICATION
    # --------------------------------------------------------

    high_risk_threshold = min(
        adaptive_threshold + 30,
        90
    )


    if risk_score >= high_risk_threshold:

        risk_level = "High Risk"

    elif risk_score >= adaptive_threshold:

        risk_level = "Suspicious"

    else:

        risk_level = "Normal"


    if not reasons:

        reasons.append(
            "Transaction behavior appears normal"
        )


    return {

        "risk_score":
        risk_score,

        "risk_level":
        risk_level,

        "adaptive_threshold":
        adaptive_threshold,

        "high_risk_threshold":
        high_risk_threshold,

        "explanation":
        reasons
    }