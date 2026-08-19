\# System Architecture



\## 1. Architecture Overview



The Adaptive AI-Based Financial Anomaly Detection System follows a layered architecture consisting of the data layer, detection layer, database layer, backend API layer, frontend layer, and adaptive feedback layer.



The architecture is designed to allow financial transactions to move through the system from detection to visualization and then back through administrator feedback for adaptive improvement.



\## 2. High-Level Architecture



```text

&#x20;                   ┌─────────────────────────┐

&#x20;                   │   Financial Dataset     │

&#x20;                   │   15,000 Transactions    │

&#x20;                   └────────────┬────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌─────────────────────────┐

&#x20;                   │ Data Validation \&       │

&#x20;                   │ Preprocessing            │

&#x20;                   └────────────┬────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌─────────────────────────┐

&#x20;                   │ Anomaly Detection \&     │

&#x20;                   │ Risk Scoring             │

&#x20;                   └────────────┬────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌─────────────────────────┐

&#x20;                   │      SQLite Database    │

&#x20;                   │ Transactions + Feedback │

&#x20;                   └────────────┬────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌─────────────────────────┐

&#x20;                   │       FastAPI           │

&#x20;                   │       Backend           │

&#x20;                   └────────────┬────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌─────────────────────────┐

&#x20;                   │      React Dashboard    │

&#x20;                   │                         │

&#x20;                   │ Summary | Anomalies     │

&#x20;                   │ Risk Distribution       │

&#x20;                   │ Feedback | Analysis     │

&#x20;                   └────────────┬────────────┘

&#x20;                                │

&#x20;                        Administrator

&#x20;                           Feedback

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌─────────────────────────┐

&#x20;                   │ Adaptive Feedback       │

&#x20;                   │ Mechanism               │

&#x20;                   └────────────┬────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌─────────────────────────┐

&#x20;                   │ Updated Risk Threshold  │

&#x20;                   └─────────────────────────┘

