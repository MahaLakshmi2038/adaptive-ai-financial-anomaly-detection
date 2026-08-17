# Adaptive AI-Based Financial Anomaly Detection System for SMEs

## Team Members

| Name | ID Number |
|---|---|
| MahaLakshmi | 2420030313 |
| Sreehitha | 2420030410 |
| Lahari | 2420030055 |

## Supervisor

[Supervisor Name]

---

## Abstract

Small and Medium Enterprises (SMEs) increasingly conduct their operations through digital transactions but rarely have access to enterprise-grade fraud and anomaly detection tools, leaving irregular cash flow, invoicing, and payment activity largely unmonitored. This project proposes a web-based Adaptive AI-Based Financial Anomaly Detection System that combines machine learning with statistical and behavioral analysis to flag unusual SME financial transactions. Its central objective is to build an SME-specific behavioral baseline that reflects the normal transaction patterns of an individual business rather than applying generic, one-size-fits-all thresholds. Anomaly scoring uses a hybrid methodology that integrates the Isolation Forest algorithm (via Scikit-learn) with statistical measures computed using Pandas and NumPy, allowing the system to identify both isolated outlier transactions and gradual behavioural drift. The core novelty of the work is its feedback-driven adaptation mechanism: administrators review flagged anomalies and label them as genuine or false positives, and this feedback is used to progressively refine the SME’s baseline and improve detection quality over time. As an Adaptive Software Engineering project, development follows an Agile methodology, with Jira used to manage the product backlog, user stories, sprint planning, and task and bug tracking across iterations. The system is implemented with a React.js frontend and a Python FastAPI backend, with transaction and feedback data stored in an SQLite database, Postman used for API testing, and Git/GitHub used for version control. The expected outcome is a working prototype that demonstrates more business-specific and adaptive anomaly detection than static rule-based approaches, giving SME administrators an interpretable tool for monitoring financial irregularities within a short academic development timeframe.

---

## Problem Statement

Small and Medium Enterprises generate a large volume of digital financial transactions but may not have access to advanced anomaly detection systems. Static rule-based approaches often use fixed thresholds that may not reflect the normal financial behaviour of different businesses.

This project aims to develop an adaptive system that learns the transaction behaviour of an individual SME and identifies transactions that significantly deviate from its established behavioural patterns.

---

## Objectives

- Detect unusual SME financial transactions using machine learning.
- Establish an SME-specific behavioural baseline.
- Combine machine learning with statistical and behavioural analysis.
- Generate an anomaly/risk score for transactions.
- Classify transactions based on risk level.
- Provide feedback-based adaptation.
- Provide an accessible dashboard for monitoring detected anomalies.

---

## Key Features

- SME-specific behavioural baseline
- AI-based anomaly detection using Isolation Forest
- Hybrid machine learning and statistical anomaly scoring
- Normal, Suspicious, and High Risk classification
- Administrator feedback on detected anomalies
- Feedback-driven adaptive detection
- Financial anomaly monitoring dashboard

---

## Novelty

### 1. SME-Specific Adaptive Behavioural Baseline
The system learns the normal transaction behaviour of an individual SME instead of applying the same fixed thresholds to every business.

### 2. Hybrid Anomaly Detection
Machine-learning-based detection is combined with statistical and behavioural analysis to generate a more meaningful anomaly score.

### 3. Feedback-Driven Adaptation
Administrator feedback on detected anomalies is stored and used to refine the SME-specific behavioural baseline and improve future detection.

---

## Methodology

```text
Financial Transaction Data
            ↓
     Data Preprocessing
            ↓
      Feature Engineering
            ↓
 SME Behavioural Baseline
            ↓
 Isolation Forest + Statistical Analysis
            ↓
       Anomaly Score
            ↓
    Risk Classification
            ↓
 Normal / Suspicious / High Risk
            ↓
 Administrator Feedback
            ↓
    Adaptive Update
            ↓
 Improved Future Detection
