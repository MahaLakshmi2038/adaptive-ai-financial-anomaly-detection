# Adaptive AI-Based Financial Anomaly Detection System for SMEs

## Project Overview

The Adaptive AI-Based Financial Anomaly Detection System is an intelligent financial monitoring solution designed to help Small and Medium-sized Enterprises (SMEs) identify suspicious and anomalous transactions.

The system combines automated anomaly detection, risk scoring, SQLite-based transaction storage, a FastAPI backend, a React dashboard, and administrator feedback.

Unlike a static detection system, the proposed solution includes an adaptive feedback mechanism that allows the risk detection threshold to change based on administrator feedback.

---

## Problem Statement

Financial fraud and anomalous transactions can cause significant financial losses for SMEs. Traditional rule-based systems often use fixed thresholds and may generate excessive false positives or fail to adapt when transaction behavior changes.

The proposed system addresses this problem by combining automated transaction analysis with administrator feedback to create a more adaptive financial anomaly detection process.

---

## Objectives

The main objectives of the project are:

1. Detect suspicious financial transactions.
2. Generate risk scores for transactions.
3. Classify transactions according to risk level.
4. Provide a dashboard for monitoring detected anomalies.
5. Store transaction and feedback information using SQLite.
6. Allow administrators to provide feedback on detected anomalies.
7. Adapt the risk threshold based on administrator feedback.
8. Provide REST APIs for system integration.
9. Provide a simple interface for analyzing individual transactions.
10. Support continuous improvement of financial monitoring.

---

## Key Features

### 1. Financial Anomaly Detection

The system analyzes transaction characteristics and identifies unusual financial behavior.

### 2. Risk Scoring

Transactions receive risk scores that are used to classify them into different risk levels.

### 3. Adaptive Feedback

Administrators can classify detected transactions as:

- Genuine Anomaly
- False Positive

The feedback is used to update the system's adaptive configuration.

### 4. Adaptive Threshold

The system maintains a risk threshold that can change based on administrator feedback.

During testing:

- Previous threshold: 40
- Updated threshold: 45

### 5. SQLite Database

Transaction results, administrator feedback, and adaptive configuration are stored using SQLite.

### 6. FastAPI Backend

The backend exposes REST APIs for communication between the database, detection system, and frontend.

### 7. React Dashboard

The dashboard displays:

- Total transactions
- Normal transactions
- Suspicious transactions
- High-risk transactions
- Adaptive threshold
- Administrator feedback count
- Detected anomalies
- Risk distribution
- Transaction analysis

### 8. Swagger API Documentation

FastAPI automatically provides interactive Swagger documentation for testing the backend APIs.

---

## System Architecture

```text
                    Financial Dataset
                           |
                           v
                Data Validation
                           |
                           v
              Anomaly Detection
                           |
                           v
                 Risk Scoring
                           |
                           v
                  SQLite Database
                           |
                           v
                   FastAPI Backend
                           |
                           v
                  React Dashboard
                           |
                    Administrator
                       Feedback
                           |
                           v
              Adaptive Feedback Engine
                           |
                           v
                Updated Risk Threshold