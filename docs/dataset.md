\# Dataset Description



\## Dataset Overview



The project uses a financial transaction dataset containing 15,000 transaction records. The dataset is used to develop and evaluate the Adaptive AI-Based Financial Anomaly Detection System for SMEs.



The dataset contains transaction-level financial, behavioral, device, network, and temporal information.



\## Dataset Features



| Feature | Description |

|---|---|

| Transaction\_ID | Unique identifier for each transaction |

| Timestamp | Date and time of the transaction |

| Customer\_ID | Identifier of the customer |

| Amount | Transaction amount |

| Merchant\_Category | Category of the merchant |

| Distance\_from\_Home | Distance between transaction location and customer's home |

| Device\_Type | Device used for the transaction |

| IP\_Risk\_Score | Risk score associated with the transaction IP address |

| Avg\_Spending\_Habit | Average spending behavior of the customer |

| Is\_Weekend | Indicates whether the transaction occurred on a weekend |

| Is\_Night\_Transaction | Indicates whether the transaction occurred during night hours |

| Is\_Fraud | Ground-truth fraud indicator |



\## Dataset Statistics



\- Total transactions: 15,000

\- Total features: 12

\- Missing values: 0

\- Normal transactions: 13,165

\- Fraudulent transactions: 1,835



\## Merchant Categories



The dataset contains the following merchant categories:



\- Groceries

\- Food\_Dining

\- Transport

\- Electronics

\- Online\_Services

\- Luxury\_Goods



\## Device Types



Transactions were performed using:



\- Android

\- iOS

\- Web\_Browser



\## Data Validation



Before model development, the dataset was validated using Pandas.



The validation confirmed:



1\. The dataset contains 15,000 records.

2\. All expected columns are present.

3\. No missing values are present.

4\. Categorical and numerical features are available for behavioral analysis.

5\. The fraud distribution was inspected before anomaly detection.



\## Role in the Proposed System



The dataset provides the transaction information required by the anomaly detection pipeline.



The system uses transaction amount, spending behavior, distance, IP risk, device information, merchant category, and temporal behavior to identify unusual transaction patterns.



The `Is\_Fraud` field is retained as a reference label for evaluation and analysis. The anomaly detection process itself is designed to identify unusual behavior rather than relying only on the fraud label.



\## Data Privacy



The project uses a prepared academic dataset. No credentials, API keys, confidential institutional information, or personally identifiable financial records are included in the repository.

