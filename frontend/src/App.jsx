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
      const summaryResponse = await fetch(`${API}/summary`);
      const anomalyResponse = await fetch(`${API}/anomalies`);
      const adaptiveResponse = await fetch(`${API}/adaptive-status`);

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

async function submitFeedback(transactionId, label) {
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

    const updatedStatus = await fetch(`${API}/adaptive-status`);
    const updatedData = await updatedStatus.json();

    setAdaptiveStatus(updatedData);

    setMessage(
      `${transactionId}: marked as ${label}`
    );
  } catch {
    setMessage("Could not submit feedback.");
  }
}
async function analyzeTransaction(e) {
  e.preventDefault();

  try {
    const params = new URLSearchParams({
      amount: form.amount,
      distance_from_home: form.distance_from_home,
      ip_risk_score: form.ip_risk_score,
      avg_spending_habit: form.avg_spending_habit,
      is_weekend: form.is_weekend,
      is_night_transaction: form.is_night_transaction,
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

    const data = await response.json();

    setAnalysis(data);
    setMessage("Transaction analyzed successfully.");
  } catch {
    setMessage("Could not analyze transaction.");
  }
}
  return (
    <div className="app">

      <header>
        <h1>Adaptive Financial Anomaly Detection</h1>
        <p>AI-powered financial monitoring for SMEs</p>
      </header>

      {message && (
        <div className="message">
          {message}
        </div>
      )}

      <section className="cards">

        <div className="card">
          <h3>Total Transactions</h3>
          <p>{summary?.total_transactions ?? "—"}</p>
        </div>

        <div className="card">
          <h3>Normal</h3>
          <p>{summary?.normal ?? "—"}</p>
        </div>

        <div className="card">
          <h3>Suspicious</h3>
          <p>{summary?.suspicious ?? "—"}</p>
        </div>

        <div className="card">
          <h3>High Risk</h3>
          <p>{summary?.high_risk ?? "—"}</p>
        </div>
        
        <div className="card">
  <h3>Adaptive Threshold</h3>
  <p>{adaptiveStatus?.risk_threshold ?? "—"}</p>
</div>

<div className="card">
  <h3>Admin Feedback</h3>
  <p>{adaptiveStatus?.feedback_count ?? "—"}</p>
</div>

      </section>
<section className="panel">

  <h2>Analyze New Transaction</h2>

  <form onSubmit={analyzeTransaction}>

    <input
      type="number"
      placeholder="Transaction Amount"
      value={form.amount}
      onChange={(e) =>
        setForm({ ...form, amount: e.target.value })
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
          distance_from_home: e.target.value,
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
          ip_risk_score: e.target.value,
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
          avg_spending_habit: e.target.value,
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
            is_weekend: e.target.checked ? 1 : 0,
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
            is_night_transaction: e.target.checked ? 1 : 0,
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

      <h3>Analysis Result</h3>

      <p>
        Risk Score: <strong>{analysis.risk_score}</strong>
      </p>

      <p>
        Risk Level: <strong>{analysis.risk_level}</strong>
      </p>

    </div>
  )}

</section>
      <section className="panel">

        <h2>Detected Anomalies</h2>

        {anomalies.length === 0 ? (
          <p>No anomalies available.</p>
        ) : (

          <table>

            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>Amount</th>
                <th>Category</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Admin Feedback</th>
              </tr>
            </thead>

            <tbody>

              {anomalies.slice(0, 20).map((item) => (

                <tr key={item.transaction_id}>

                  <td>{item.transaction_id}</td>

                  <td>₹{item.amount}</td>

                  <td>{item.merchant_category}</td>

                  <td>{item.risk_score}</td>

                  <td>{item.risk_level}</td>

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

    </div>
  );
}

export default App;