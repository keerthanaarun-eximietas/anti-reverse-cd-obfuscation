
import { useState } from "react";
import { Send, ShieldCheck } from "lucide-react";
import { createTransaction } from "../services/api";

const initialForm = {
  customer: "",
  amount: "1000",
  currency: "INR",
  country: "IN",
  account_country: "IN",
  failed_attempts: "0",
  account_age_days: "30",
};

export default function TransactionForm({ onCreated }) {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await createTransaction({
        ...form,
        amount: Number(form.amount),
        failed_attempts: Number(form.failed_attempts),
        account_age_days: Number(form.account_age_days),
      });

      setResult(data.transaction);
      setForm(initialForm);
      await onCreated();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel form-panel">
      <div className="form-heading">
        <div>
          <p className="panel-label">TRANSACTION INPUT</p>
          <h2>Evaluate a New Transaction</h2>
          <p>Enter sample transaction details to calculate its risk.</p>
        </div>
        <div className="panel-icon">
          <ShieldCheck size={21} />
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <label>
            Customer
            <input
              name="customer"
              value={form.customer}
              onChange={updateField}
              placeholder="e.g. Customer F"
              required
            />
          </label>

          <label>
            Amount
            <input
              name="amount"
              type="number"
              min="0.01"
              step="0.01"
              value={form.amount}
              onChange={updateField}
              required
            />
          </label>

          <label>
            Currency
            <select
              name="currency"
              value={form.currency}
              onChange={updateField}
            >
              <option value="INR">INR</option>
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="GBP">GBP</option>
            </select>
          </label>

          <label>
            Transaction country
            <input
              name="country"
              value={form.country}
              onChange={updateField}
              maxLength="2"
              placeholder="IN"
              required
            />
          </label>

          <label>
            Account country
            <input
              name="account_country"
              value={form.account_country}
              onChange={updateField}
              maxLength="2"
              placeholder="IN"
              required
            />
          </label>

          <label>
            Failed attempts
            <input
              name="failed_attempts"
              type="number"
              min="0"
              step="1"
              value={form.failed_attempts}
              onChange={updateField}
              required
            />
          </label>

          <label>
            Account age (days)
            <input
              name="account_age_days"
              type="number"
              min="0"
              step="1"
              value={form.account_age_days}
              onChange={updateField}
              required
            />
          </label>
        </div>

        <button className="submit-button" type="submit" disabled={loading}>
          <Send size={16} />
          {loading ? "Evaluating..." : "Evaluate Transaction"}
        </button>
      </form>

      {error && <div className="form-error">{error}</div>}

      {result && (
        <div className="result-panel">
          <h3>Risk assessment completed</h3>
          <p>
            Transaction: <strong>{result.id}</strong>
          </p>
          <p>
            Risk score: <strong>{result.risk_score}/90</strong>
          </p>
          <p>
            Risk level: <strong>{result.risk_level}</strong>
          </p>
          <p>
            Decision: <strong>{result.decision}</strong>
          </p>
          <p>
            Reasons:{" "}
            <strong>
              {result.reasons.length
                ? result.reasons.join(", ")
                : "No risk rules triggered"}
            </strong>
          </p>
        </div>
      )}
    </section>
  );
}
