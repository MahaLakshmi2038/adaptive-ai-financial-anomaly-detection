import { useEffect, useState } from "react";
import "./App.css";

function App() {

  const [summary, setSummary] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [adaptiveStatus, setAdaptiveStatus] = useState(null);
  const [message, setMessage] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const [form, setForm] = useState({
    amount: "",
    distance_from_home: "",
    ip_risk_score: "",
    avg_spending_habit: "",
    is_weekend: 0,
    is_night_transaction: 0,
  });

  const API = "http://127.0.0.1:8000";

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {

    try {

      const [
        summaryResponse,
        anomalyResponse,
        adaptiveResponse
      ] = await Promise.all([
        fetch(`${API}/summary`),
        fetch(`${API}/anomalies`),
        fetch(`${API}/adaptive-status`)
      ]);

      const summaryData = await summaryResponse.json();
      const anomalyData = await anomalyResponse.json();
      const adaptiveData = await adaptiveResponse.json();

      setSummary(summaryData);
      setAnomalies(anomalyData);
      setAdaptiveStatus(adaptiveData);

    } catch {

      setMessage("Backend is not running.");

    }
  }


  async function submitFeedback(
    transactionId,
    label
  ) {

    try {

      const response = await fetch(
        `${API}/feedback?transaction_id=${encodeURIComponent(transactionId)}&admin_label=${encodeURIComponent(label)}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error();
      }

      const updatedStatus =
        await fetch(`${API}/adaptive-status`);

      const updatedData =
        await updatedStatus.json();

      setAdaptiveStatus(updatedData);

      setMessage(
        `${transactionId}: marked as ${label}. System adapted.`
      );

    } catch {

      setMessage(
        "Could not submit feedback."
      );

    }
  }


  async function analyzeTransaction(e) {

    e.preventDefault();

    try {

      const params = new URLSearchParams({
        amount: form.amount,
        distance_from_home:
          form.distance_from_home,
        ip_risk_score:
          form.ip_risk_score,
        avg_spending_habit:
          form.avg_spending_habit,
        is_weekend:
          form.is_weekend,
        is_night_transaction:
          form.is_night_transaction,
      });

      const response = await fetch(
        `${API}/analyze?${params.toString()}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error();
      }

      const data =
        await response.json();

      setAnalysis(data);

      setMessage(
        "Transaction analyzed successfully."
      );

    } catch {

      setMessage(
        "Could not analyze transaction."
      );

    }
  }


  return (

    <div className="app">

      <header>

        <h1>
          Adaptive Financial Anomaly Detection
        </h1>

        <p>
          AI-powered adaptive financial risk
          monitoring for SMEs
        </p>

      </header>


      {message && (
        <div className="message">
          {message}
        </div>
      )}


      {/* =====================================================
          SUMMARY CARDS
      ===================================================== */}

      <section className="cards">

        <div className="card">
          <h3>Total Transactions</h3>
          <p>
            {summary?.total_transactions ?? "—"}
          </p>
        </div>

        <div className="card">
          <h3>Normal</h3>
          <p>
            {summary?.normal ?? "—"}
          </p>
        </div>

        <div className="card">
          <h3>Suspicious</h3>
          <p>
            {summary?.suspicious ?? "—"}
          </p>
        </div>

        <div className="card">
          <h3>High Risk</h3>
          <p>
            {summary?.high_risk ?? "—"}
          </p>
        </div>

        <div className="card">
          <h3>Adaptive Threshold</h3>
          <p>
            {adaptiveStatus?.risk_threshold ?? "—"}
          </p>
        </div>

        <div className="card">
          <h3>Admin Feedback</h3>
          <p>
            {adaptiveStatus?.feedback_count ?? "—"}
          </p>
        </div>

      </section>


      {/* =====================================================
          ADAPTIVE ENGINE STATUS
      ===================================================== */}

      <section className="panel">

        <h2>🧠 Adaptive Risk Engine</h2>

        <div className="cards">

          <div className="card">

            <h3>System Status</h3>

            <p>
              {adaptiveStatus
                ? "ACTIVE"
                : "—"}
            </p>

          </div>


          <div className="card">

            <h3>Genuine Anomalies</h3>

            <p>
              {adaptiveStatus?.genuine_anomalies ?? "—"}
            </p>

          </div>


          <div className="card">

            <h3>False Positives</h3>

            <p>
              {adaptiveStatus?.false_positives ?? "—"}
            </p>

          </div>


          <div className="card">

            <h3>False Positive Rate</h3>

            <p>
              {adaptiveStatus?.false_positive_rate ?? 0}%
            </p>

          </div>

        </div>

        <p>
          The system continuously uses administrator
          feedback to recalibrate future risk decisions.
        </p>

      </section>


      {/* =====================================================
          RISK DISTRIBUTION
      ===================================================== */}

      <section className="panel">

        <h2>📊 Risk Distribution</h2>

        <div className="risk-chart">

          <div className="risk-bar">

            <span>Normal</span>

            <div
              className="bar normal"
              style={{
                width: `${
                  summary
                    ? (
                        summary.normal /
                        summary.total_transactions
                      ) * 100
                    : 0
                }%`,
              }}
            >
              {summary?.normal ?? 0}
            </div>

          </div>


          <div className="risk-bar">

            <span>Suspicious</span>

            <div
              className="bar suspicious"
              style={{
                width: `${
                  summary
                    ? (
                        summary.suspicious /
                        summary.total_transactions
                      ) * 100
                    : 0
                }%`,
              }}
            >
              {summary?.suspicious ?? 0}
            </div>

          </div>


          <div className="risk-bar">

            <span>High Risk</span>

            <div
              className="bar high-risk"
              style={{
                width: `${
                  summary
                    ? (
                        summary.high_risk /
                        summary.total_transactions
                      ) * 100
                    : 0
                }%`,
              }}
            >
              {summary?.high_risk ?? 0}
            </div>

          </div>

        </div>

      </section>


      {/* =====================================================
          BEHAVIORAL ANALYSIS
      ===================================================== */}

      <section className="panel">

        <h2>🔎 Analyze New Transaction</h2>

        <form onSubmit={analyzeTransaction}>

          <input
            type="number"
            placeholder="Transaction Amount"
            value={form.amount}
            onChange={(e) =>
              setForm({
                ...form,
                amount: e.target.value
              })
            }
            required
          />


          <input
            type="number"
            placeholder="Distance From Home"
            value={form.distance_from_home}
            onChange={(e) =>
              setForm({
                ...form,
                distance_from_home:
                  e.target.value
              })
            }
            required
          />


          <input
            type="number"
            placeholder="IP Risk Score (0-100)"
            value={form.ip_risk_score}
            onChange={(e) =>
              setForm({
                ...form,
                ip_risk_score:
                  e.target.value
              })
            }
            required
          />


          <input
            type="number"
            placeholder="Average Spending Habit"
            value={form.avg_spending_habit}
            onChange={(e) =>
              setForm({
                ...form,
                avg_spending_habit:
                  e.target.value
              })
            }
            required
          />


          <label>

            <input
              type="checkbox"
              onChange={(e) =>
                setForm({
                  ...form,
                  is_weekend:
                    e.target.checked ? 1 : 0
                })
              }
            />

            Weekend Transaction

          </label>


          <label>

            <input
              type="checkbox"
              onChange={(e) =>
                setForm({
                  ...form,
                  is_night_transaction:
                    e.target.checked ? 1 : 0
                })
              }
            />

            Night Transaction

          </label>


          <button type="submit">
            Analyze Transaction
          </button>

        </form>


        {analysis && (

          <div className="analysis-result">

            <h3>
              Analysis Result
            </h3>

            <p>
              Risk Score:
              <strong>
                {" "}
                {analysis.risk_score}
              </strong>
            </p>


            <p>
              Risk Level:
              <strong>
                {" "}
                {analysis.risk_level}
              </strong>
            </p>


            <p>
              Adaptive Threshold:
              <strong>
                {" "}
                {analysis.adaptive_threshold}
              </strong>
            </p>


            <p>
              High Risk Threshold:
              <strong>
                {" "}
                {analysis.high_risk_threshold}
              </strong>
            </p>


            <h4>
              Why was this transaction flagged?
            </h4>


            <ul>

              {analysis.explanation?.map(
                (reason, index) => (
                  <li key={index}>
                    {reason}
                  </li>
                )
              )}

            </ul>

          </div>

        )}

      </section>


      {/* =====================================================
          DETECTED ANOMALIES
      ===================================================== */}

      <section className="panel">

        <h2>
          🚨 Detected Anomalies
        </h2>


        {anomalies.length === 0 ? (

          <p>
            No anomalies available.
          </p>

        ) : (

          <table>

            <thead>

              <tr>

                <th>
                  Transaction ID
                </th>

                <th>
                  Amount
                </th>

                <th>
                  Category
                </th>

                <th>
                  Risk Score
                </th>

                <th>
                  Risk Level
                </th>

                <th>
                  Why Flagged
                </th>

                <th>
                  Admin Decision
                </th>

              </tr>

            </thead>


            <tbody>

              {anomalies
                .slice(0, 20)
                .map((item) => (

                  <tr
                    key={item.transaction_id}
                  >

                    <td>
                      {item.transaction_id}
                    </td>


                    <td>
                      ₹{item.amount}
                    </td>


                    <td>
                      {item.merchant_category}
                    </td>


                    <td>
                      {item.risk_score}
                    </td>


                    <td>
                      {item.risk_level}
                    </td>


                    <td>
                      {item.risk_explanation}
                    </td>


                    <td>

                      <button
                        onClick={() =>
                          submitFeedback(
                            item.transaction_id,
                            "Genuine Anomaly"
                          )
                        }
                      >
                        Genuine
                      </button>


                      <button
                        onClick={() =>
                          submitFeedback(
                            item.transaction_id,
                            "False Positive"
                          )
                        }
                      >
                        False Positive
                      </button>

                    </td>

                  </tr>

                ))}

            </tbody>

          </table>

        )}

      </section>


      {/* =====================================================
          DRIFT MONITOR
      ===================================================== */}

      {anomalies.length > 0 && (

        <section className="panel">

          <h2>
            📈 Behavioral Drift Monitor
          </h2>

          <p>
            Historical anomaly rate:
            <strong>
              {" "}
              {anomalies[0]
                ?.historical_anomaly_rate ?? 0}%
            </strong>
          </p>


          <p>
            Recent anomaly rate:
            <strong>
              {" "}
              {anomalies[0]
                ?.recent_anomaly_rate ?? 0}%
            </strong>
          </p>


          <p>
            Drift status:
            <strong>
              {" "}
              {anomalies[0]
                ?.drift_status ?? "Stable"}
            </strong>
          </p>

        </section>

      )}

    </div>
  );
}

export default App;