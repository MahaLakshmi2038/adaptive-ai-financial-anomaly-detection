\# API Documentation



\## 1. API Overview



The backend of the Adaptive AI-Based Financial Anomaly Detection System is implemented using FastAPI.



The API provides communication between the React frontend, the SQLite database, and the anomaly detection system.



Base URL:



http://127.0.0.1:8000



Interactive Swagger documentation:



http://127.0.0.1:8000/docs



\## 2. GET /summary



\### Purpose



Returns an overall summary of the financial transaction analysis.



\### Response Information



The endpoint provides information such as:



\- Total transactions

\- Normal transactions

\- Suspicious transactions

\- High-risk transactions



\### Example



```text

GET /summary

