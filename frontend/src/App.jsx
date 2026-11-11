
import { useEffect, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowDownRight,
  ArrowUpRight,
  CheckCircle2,
  Clock3,
  RefreshCw,
  ShieldCheck,
  XCircle,
} from "lucide-react";
import TransactionForm from "./components/TransactionForm";
import { getSummary, getTransactions } from "./services/api";
import "./styles/index.css";

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(amount);
}

function StatCard({ title, value, subtitle, icon: Icon, type }) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${type}`}>
        <Icon size={21} />
      </div>
      <div className="stat-content">
        <p>{title}</p>
        <h2>{value}</h2>
        <span>{subtitle}</span>
      </div>
    </div>
  );
}

function DecisionBadge({ decision }) {
  const styles = {
    APPROVE: "approved",
    REVIEW: "review",
    REJECT: "rejected",
  };

  return (
    <span className={`decision-badge ${styles[decision] || ""}`}>
      {decision || "PENDING"}
    </span>
  );
}

function App() {
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard(showLoading = true) {
    try {
      if (showLoading) setLoading(true);
      setError("");

      const [transactionData, summaryData] = await Promise.all([
        getTransactions(),
        getSummary(),
      ]);

      setTransactions(transactionData.transactions);
      setSummary(summaryData);
    } catch (err) {
      setError(
        "Unable to connect to the backend. Make sure Flask is running on port 5000."
      );
    } finally {
      if (showLoading) setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <ShieldCheck size={25} />
          </div>
          <div>
            <h2>Sentinel</h2>
            <span>Risk Intelligence</span>
          </div>
        </div>

        <div className="nav-section">
          <p className="nav-label">WORKSPACE</p>
          <div className="nav-item active">
            <Activity size={18} />
            <span>Dashboard</span>
          </div>
          <div className="nav-item">
            <Clock3 size={18} />
            <span>Transactions</span>
          </div>
          <div className="nav-item">
            <AlertTriangle size={18} />
            <span>Risk Analysis</span>
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="system-status">
            <span className="status-dot"></span>
            Backend connected
          </div>
          <p>Research prototype · v1.0</p>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="breadcrumb">Workspace / Overview</p>
            <h1>Transaction Dashboard</h1>
            <p className="page-description">
              Monitor transactions and identify potentially suspicious activity.
            </p>
          </div>

          <button className="refresh-button" onClick={loadDashboard}>
            <RefreshCw size={16} />
            Refresh
          </button>
        </header>

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loading">Loading transaction data...</div>
        ) : (
          <>
            <section className="stats-grid">
              <StatCard
                title="Total Transactions"
                value={summary?.total_transactions ?? 0}
                subtitle="Transactions processed"
                icon={Activity}
                type="blue"
              />
              <StatCard
                title="Approved"
                value={summary?.decisions?.APPROVE ?? 0}
                subtitle="Low-risk transactions"
                icon={CheckCircle2}
                type="green"
              />
              <StatCard
                title="Needs Review"
                value={summary?.decisions?.REVIEW ?? 0}
                subtitle="Requires investigation"
                icon={AlertTriangle}
                type="orange"
              />
              <StatCard
                title="Rejected"
                value={summary?.decisions?.REJECT ?? 0}
                subtitle="High-risk transactions"
                icon={XCircle}
                type="red"
              />
            </section>

            <section className="overview-grid">
              <div className="panel total-value-panel">
                <div className="panel-heading">
                  <div>
                    <p className="panel-label">TRANSACTION VALUE</p>
                    <h2>
                      {formatCurrency(summary?.total_transaction_value ?? 0)}
                    </h2>
                  </div>
                  <div className="panel-icon">
                    <ArrowUpRight size={21} />
                  </div>
                </div>
                <p className="panel-note">
                  Combined value of all transactions in the current session.
                </p>
              </div>

              <div className="panel risk-panel">
                <div className="panel-heading">
                  <div>
                    <p className="panel-label">RISK MONITORING</p>
                    <h2>Active</h2>
                  </div>
                  <div className="panel-icon green">
                    <ShieldCheck size={21} />
                  </div>
                </div>
                <p className="panel-note">
                  Rule-based transaction risk assessment is operational.
                </p>
              </div>
            </section>

            <TransactionForm onCreated={() => loadDashboard(false)} />

            <section className="panel transactions-panel">
              <div className="table-heading">
                <div>
                  <h2>Recent Transactions</h2>
                  <p>Review transaction activity and risk decisions.</p>
                </div>
                <span className="record-count">
                  {transactions.length} records
                </span>
              </div>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Transaction ID</th>
                      <th>Customer</th>
                      <th>Amount</th>
                      <th>Location</th>
                      <th>Risk Score</th>
                      <th>Decision</th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.map((transaction) => (
                      <tr key={transaction.id}>
                        <td className="transaction-id">{transaction.id}</td>
                        <td>{transaction.customer}</td>
                        <td className="amount">
                          {formatCurrency(transaction.amount)}
                        </td>
                        <td>{transaction.country}</td>
                        <td>
                          <div className="risk-score">
                            <span>{transaction.risk_score}</span>
                            <span className="score-out-of">/ 90</span>
                          </div>
                        </td>
                        <td>
                          <DecisionBadge decision={transaction.decision} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {transactions.length === 0 && (
                  <p className="empty-state">No transactions available.</p>
                )}
              </div>
            </section>

            <footer className="footer">
              <span>Sentinel Risk Intelligence</span>
              <span>
                <ArrowDownRight size={13} />
                Data resets when the backend restarts
              </span>
            </footer>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
