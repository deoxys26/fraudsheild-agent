import { useState } from "react";
import { updateCollectedDetails } from "../api/api";

function ResultCard({ result }) {
  const [collectedDetails, setCollectedDetails] = useState({});
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  if (!result) {
    return (
      <div className="panel empty">
        <h2>Complaint Result</h2>
        <p className="muted">Submit a complaint to receive your ticket details.</p>
      </div>
    );
  }

  const handleDetailChange = (detail, value) => {
    setCollectedDetails((prev) => ({
      ...prev,
      [detail]: value,
    }));
  };

  const handleSubmitDetails = async () => {
    try {
      setSaving(true);
      await updateCollectedDetails(result.ticket_id, collectedDetails);
      setSaved(true);
    } catch (error) {
      console.error("Failed to submit details", error);
      alert("Could not submit details. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="panel">
      <div className="result-header">
        <div>
          <h2>{result.ticket_id}</h2>
          <p className="muted">{result.category}</p>
        </div>
        <span className="badge medium">{result.status}</span>
      </div>

      <div className="customer-box">
        <div>
          <span>Customer</span>
          <strong>{result.customer_name || "Not provided"}</strong>
        </div>
        <div>
          <span>Account Last 4</span>
          <strong>{result.account_last4 || "N/A"}</strong>
        </div>
        <div>
          <span>Phone</span>
          <strong>{result.phone || "N/A"}</strong>
        </div>
      </div>

      <div className="metrics">
        <div>
          <span>Amount</span>
          <strong>₹{result.amount}</strong>
        </div>
        <div>
          <span>Status</span>
          <strong>{result.status}</strong>
        </div>
        <div>
          <span>Category</span>
          <strong>{result.category}</strong>
        </div>
      </div>

      <section>
        <h3>Details Required</h3>
        <p className="muted">
          Please provide the following details to help the bank process your complaint faster.
        </p>

        <div className="detail-input-list">
          {result.missing_details?.map((detail, index) => (
            <div className="detail-input-row" key={index}>
              <label>{detail}</label>
              <input
                value={collectedDetails[detail] || ""}
                onChange={(e) => handleDetailChange(detail, e.target.value)}
                placeholder={`Enter ${detail}`}
              />
            </div>
          ))}
        </div>

        <button
          className="submit-details-btn"
          onClick={handleSubmitDetails}
          disabled={saving}
        >
          {saving ? "Submitting..." : "Submit Details"}
        </button>

        {saved && (
          <p className="success-text">
            Details submitted successfully. Please save your ticket ID for tracking.
          </p>
        )}
      </section>

      <section>
        <h3>Next Step</h3>
        <p>
          Your complaint has been registered. Please save your ticket ID. A bank officer
          will review your case and may contact you if more verification is needed.
        </p>
      </section>
    </div>
  );
}

export default ResultCard;