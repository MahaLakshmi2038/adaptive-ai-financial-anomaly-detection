import pandas as pd
import os

RESULTS_FILE = "results/anomaly_results.csv"
FEEDBACK_FILE = "results/feedback.csv"


# ------------------------------------------------------------
# 1. LOAD DETECTION RESULTS
# ------------------------------------------------------------

df = pd.read_csv(RESULTS_FILE)

print("Loaded anomaly results:", len(df))


# ------------------------------------------------------------
# 2. CREATE FEEDBACK FILE
# ------------------------------------------------------------

if not os.path.exists(FEEDBACK_FILE):

    feedback_columns = [
        "Transaction_ID",
        "Admin_Label"
    ]

    feedback_df = pd.DataFrame(
        columns=feedback_columns
    )

    feedback_df.to_csv(
        FEEDBACK_FILE,
        index=False
    )

    print("Feedback file created.")


# ------------------------------------------------------------
# 3. SIMULATE ADMIN FEEDBACK
# ------------------------------------------------------------

# Take some detected anomalies for demonstration.

anomalies = df[df["Anomaly"] == 1].head(10).copy()

feedback = pd.DataFrame({
    "Transaction_ID": anomalies["Transaction_ID"],
    "Admin_Label": [
        "Genuine Anomaly",
        "False Positive",
        "Genuine Anomaly",
        "Genuine Anomaly",
        "False Positive",
        "Genuine Anomaly",
        "False Positive",
        "Genuine Anomaly",
        "Genuine Anomaly",
        "False Positive"
    ][:len(anomalies)]
})


# ------------------------------------------------------------
# 4. SAVE FEEDBACK
# ------------------------------------------------------------

feedback.to_csv(
    FEEDBACK_FILE,
    mode="a",
    header=False,
    index=False
)

print("\nAdministrator feedback recorded:")
print(feedback)


# ------------------------------------------------------------
# 5. ANALYZE FEEDBACK
# ------------------------------------------------------------

feedback_data = pd.read_csv(
    FEEDBACK_FILE
)

genuine = (
    feedback_data["Admin_Label"]
    == "Genuine Anomaly"
).sum()

false_positive = (
    feedback_data["Admin_Label"]
    == "False Positive"
).sum()


print("\n--------------------------------")
print("ADAPTIVE FEEDBACK SUMMARY")
print("--------------------------------")

print(
    "Genuine anomalies:",
    genuine
)

print(
    "False positives:",
    false_positive
)


# ------------------------------------------------------------
# 6. ADAPTIVE THRESHOLD
# ------------------------------------------------------------

# Calculate false-positive rate

total_feedback = genuine + false_positive

if total_feedback > 0:

    false_positive_rate = (
        false_positive / total_feedback
    )

else:

    false_positive_rate = 0


# Start with the original threshold

base_threshold = 40


# If too many false positives are reported,
# increase the suspicious threshold.

if false_positive_rate > 0.30:

    new_threshold = base_threshold + 5

else:

    new_threshold = base_threshold


print(
    "\nPrevious threshold:",
    base_threshold
)

print(
    "Updated threshold:",
    new_threshold
)


# ------------------------------------------------------------
# 7. SAVE ADAPTIVE CONFIGURATION
# ------------------------------------------------------------

config = pd.DataFrame({
    "Parameter": [
        "Risk_Threshold"
    ],
    "Value": [
        new_threshold
    ]
})

config.to_csv(
    "results/adaptive_config.csv",
    index=False
)

print(
    "\nAdaptive configuration saved to:"
    " results/adaptive_config.csv"
)