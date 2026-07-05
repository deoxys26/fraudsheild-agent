import { useState } from "react";
import { analyzeComplaint } from "../api/api";

function ComplaintForm({ onResult, onTicketCreated }) {
  const [formData, setFormData] = useState({
    customer_name: "",
    account_last4: "",
    phone: "",
    complaint: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const examples = [
    "Customer clicked a fake KYC link and ₹80,000 was transferred from their account.",
    "Customer says ATM did not dispense cash but ₹10,000 was debited from the account.",
    "Customer says ₹25,000 was deducted through UPI but they did not authorize the transaction.",
    "Customer says a card transaction of ₹15,500 happened on an e-commerce site but they did not make it.",
    "Customer accidentally transferred ₹5,000 to the wrong UPI ID.",
  ];

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const useExample = (text) => {
    setFormData((prev) => ({
      ...prev,
      complaint: text,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!formData.complaint.trim()) {
      setError("Please enter a complaint.");
      return;
    }

    try {
      setLoading(true);
      const result = await analyzeComplaint(formData);
      onResult(result);
      onTicketCreated();
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Submit Fraud Complaint</h2>
      <p className="muted">
  Submit your complaint details. A ticket will be created and you will receive
  the required next steps for your case.
</p>

      <form onSubmit={handleSubmit} className="form">
        <div className="grid-3">
          <input
            name="customer_name"
            placeholder="Customer name"
            value={formData.customer_name}
            onChange={handleChange}
          />
          <input
            name="account_last4"
            placeholder="Account last 4 digits"
            value={formData.account_last4}
            onChange={handleChange}
            maxLength="4"
          />
          <input
            name="phone"
            placeholder="Phone number"
            value={formData.phone}
            onChange={handleChange}
          />
        </div>

        <textarea
          name="complaint"
          placeholder="Describe the complaint..."
          value={formData.complaint}
          onChange={handleChange}
          rows="5"
        />

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Complaint"}
        </button>

        {error && <p className="error">{error}</p>}
      </form>

      <div className="examples">
        <p className="muted">Try demo cases:</p>
        {examples.map((item, index) => (
          <button key={index} className="example-btn" onClick={() => useExample(item)}>
            {item}
          </button>
        ))}
      </div>
    </div>
  );
}

export default ComplaintForm;