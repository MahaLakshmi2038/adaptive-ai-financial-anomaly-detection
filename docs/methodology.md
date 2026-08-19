\# Methodology



\## 1. System Overview



The Adaptive AI-Based Financial Anomaly Detection System is designed to identify suspicious financial transactions for Small and Medium-sized Enterprises (SMEs).



The system combines anomaly detection, risk scoring, administrator feedback, and adaptive threshold adjustment to continuously improve transaction monitoring.



The overall workflow is:



Transaction Dataset  

↓  

Data Validation and Preprocessing  

↓  

Anomaly Detection  

↓  

Risk Score Generation  

↓  

Risk Classification  

↓  

Administrator Feedback  

↓  

Adaptive Threshold Update  

↓  

Updated Risk Detection  

↓  

Dashboard and API



\## 2. Data Preprocessing



The financial transaction dataset is first loaded using Pandas.



The preprocessing stage includes:



\- Loading the CSV dataset.

\- Validating the number of records and features.

\- Checking for missing values.

\- Inspecting numerical features.

\- Inspecting categorical features.

\- Examining fraud distribution.

\- Preparing transaction attributes for anomaly detection.



The dataset contains 15,000 transactions and 12 attributes, with no missing values.



\## 3. Anomaly Detection



The system analyzes transaction characteristics to identify deviations from normal financial behavior.



Important behavioral indicators include:



\- Transaction amount

\- Average spending habit

\- Distance from home

\- IP risk score

\- Device type

\- Merchant category

\- Weekend activity

\- Night-time activity



Transactions that demonstrate unusual combinations of these characteristics receive higher anomaly or risk scores.



\## 4. Risk Scoring



Each transaction is assigned a risk score based on detected suspicious characteristics.



The risk score allows transactions to be categorized into different risk levels.



The system uses the following conceptual classification:



\- Normal: Low-risk transaction

\- Suspicious: Transaction showing unusual behavior

\- High Risk: Transaction with strong indicators of anomalous behavior



This classification allows administrators to prioritize transactions that require investigation.



\## 5. Adaptive Feedback Mechanism



A key feature of the proposed system is administrator feedback.



Administrators can classify detected transactions as:



\- Genuine Anomaly

\- False Positive



This feedback is recorded by the system and used to modify the risk detection threshold.



For example, when genuine anomalies are identified, the system can become more sensitive to suspicious behavior. When excessive false positives are observed, the threshold can be adjusted to reduce unnecessary alerts.



\## 6. Adaptive Threshold



The system maintains an adaptive risk threshold.



The initial threshold is:



40



After administrator feedback was recorded during testing, the system calculated an updated threshold of:



45



The updated configuration is stored in:



`results/adaptive\_config.csv`



This demonstrates the adaptive behavior of the proposed system.



\## 7. Database Layer



SQLite is used to store system information locally.



The database stores:



\- Transaction information

\- Risk scores

\- Risk levels

\- Anomaly status

\- Administrator feedback

\- Adaptive configuration



The database allows the backend to retrieve and update transaction and feedback information efficiently.



\## 8. Backend



The backend is implemented using FastAPI.



The backend provides REST API endpoints for:



\- Transaction summaries

\- Detected anomalies

\- Adaptive status

\- Administrator feedback

\- Transaction analysis



Swagger/OpenAPI documentation is automatically provided by FastAPI for API testing.



\## 9. Frontend



The frontend is implemented using React and Vite.



The dashboard provides:



\- Total transaction count

\- Normal transaction count

\- Suspicious transaction count

\- High-risk transaction count

\- Adaptive threshold

\- Administrator feedback count

\- Detected anomaly table

\- Risk distribution visualization

\- Administrator feedback controls



The frontend communicates with the FastAPI backend through HTTP requests.



\## 10. System Integration



The complete system integrates the following components:



Dataset → Python anomaly detection → SQLite database → FastAPI backend → React dashboard.



Administrator feedback flows in the opposite direction:



React dashboard → FastAPI feedback endpoint → Database → Adaptive configuration.



This creates a feedback-driven monitoring system rather than a static anomaly detection pipeline.



\## 11. Adaptive Software Engineering Aspect



The project follows the principles of Adaptive Software Engineering by allowing the system to respond to feedback and changing detection requirements.



Instead of keeping the detection threshold fixed, administrator feedback influences the configuration of the system.



This provides a mechanism for continuous adjustment based on operational observations.



\## 12. Technologies Used



\- Python

\- Pandas

\- NumPy

\- Scikit-learn

\- SQLite

\- FastAPI

\- Uvicorn

\- React

\- Vite

\- JavaScript

\- HTML

\- CSS

\- Git

\- GitHub

\- Jira



\## 13. Final Workflow



The final system workflow is:



1\. Load financial transaction data.

2\. Validate and preprocess the dataset.

3\. Detect anomalous transaction behavior.

4\. Generate risk scores.

5\. Classify transactions by risk level.

6\. Store results in SQLite.

7\. Display results through the React dashboard.

8\. Allow administrators to provide feedback.

9\. Record feedback in the database.

10\. Update the adaptive risk threshold.

11\. Use the updated configuration for future monitoring.



The methodology enables the system to combine automated anomaly detection with human feedback, making the financial monitoring process more adaptive and suitable for evolving transaction behavior.

