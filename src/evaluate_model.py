import pandas as pd
import os


# ============================================================
# CONFIGURATION
# ============================================================

RESULTS_FILE = "results/anomaly_results.csv"
CONFIG_FILE = "results/adaptive_config.csv"


# ============================================================
# LOAD RESULTS
# ============================================================

if not os.path.exists(RESULTS_FILE):

    print("ERROR: anomaly_results.csv not found.")

    print(
        "Run: python src/anomaly_detector.py"
    )

    raise SystemExit


df = pd.read_csv(RESULTS_FILE)


print("\n========================================")
print("ADAPTIVE FINANCIAL ANOMALY DETECTION")
print("MODEL EVALUATION")
print("========================================")


# ============================================================
# BASIC STATISTICS
# ============================================================

total_transactions = len(df)

anomalies = (
    df["Anomaly"] == 1
).sum()

normal = (
    df["Risk_Level"] == "Normal"
).sum()

suspicious = (
    df["Risk_Level"] == "Suspicious"
).sum()

high_risk = (
    df["Risk_Level"] == "High Risk"
).sum()


anomaly_percentage = (
    anomalies / total_transactions
) * 100


average_risk_score = (
    df["Risk_Score"].mean()
)


maximum_risk_score = (
    df["Risk_Score"].max()
)


minimum_risk_score = (
    df["Risk_Score"].min()
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nTotal Transactions:")
print(total_transactions)


print("\nDetected Anomalies:")
print(anomalies)


print("\nAnomaly Percentage:")
print(
    round(anomaly_percentage, 2),
    "%"
)


print("\nRisk Distribution:")

print(
    "Normal:",
    normal
)

print(
    "Suspicious:",
    suspicious
)

print(
    "High Risk:",
    high_risk
)


print("\nRisk Score Statistics:")

print(
    "Average Risk Score:",
    round(
        average_risk_score,
        2
    )
)

print(
    "Minimum Risk Score:",
    round(
        minimum_risk_score,
        2
    )
)

print(
    "Maximum Risk Score:",
    round(
        maximum_risk_score,
        2
    )
)


# ============================================================
# ADAPTIVE CONFIGURATION
# ============================================================

if os.path.exists(CONFIG_FILE):

    config = pd.read_csv(
        CONFIG_FILE
    )

    threshold = config.loc[
        config["Parameter"] == "Risk_Threshold",
        "Value"
    ]

    if len(threshold) > 0:

        print(
            "\nCurrent Adaptive Threshold:"
        )

        print(
            threshold.iloc[0]
        )


# ============================================================
# SAVE EVALUATION REPORT
# ============================================================

report = pd.DataFrame({

    "Metric": [

        "Total Transactions",

        "Detected Anomalies",

        "Anomaly Percentage",

        "Normal Transactions",

        "Suspicious Transactions",

        "High Risk Transactions",

        "Average Risk Score",

        "Minimum Risk Score",

        "Maximum Risk Score"

    ],

    "Value": [

        total_transactions,

        anomalies,

        round(
            anomaly_percentage,
            2
        ),

        normal,

        suspicious,

        high_risk,

        round(
            average_risk_score,
            2
        ),

        round(
            minimum_risk_score,
            2
        ),

        round(
            maximum_risk_score,
            2
        )

    ]

})


os.makedirs(
    "results",
    exist_ok=True
)


report.to_csv(
    "results/evaluation_report.csv",
    index=False
)


print("\n========================================")

print(
    "Evaluation report saved to:"
)

print(
    "results/evaluation_report.csv"
)

print(
    "========================================")