import { useEffect, useState } from "react";
import {
  getTicketAlerts,
  getTicketAuditLogs,
  updateOfficerNote,
  updateTicketStatus,
  updateCollectedDetails,
} from "../api/api";

function TicketDetails({ ticket, onClose, onUpdated }) {
  const [alerts, setAlerts] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [status, setStatus] = useState(ticket?.status || "Open");
  const [note, setNote] = useState(ticket?.officer_note || "");
  const [saving, setSaving] = useState(false);
  const [collectedDetails, setCollectedDetails] = useState({});

  useEffect(() => {
    if (!ticket) return;

    const loadDetails = async () => {
      try {
        const [alertsData, logsData] = await Promise.all([
          getTicketAlerts(ticket.ticket_id),
          getTicketAuditLogs(ticket.ticket_id),
        ]);

        setCollectedDetails(ticket.collected_details || {});
        setAlerts(alertsData);
        setAuditLogs(logsData);
        setStatus(ticket.status);
        setNote(ticket.officer_note || "");
      } catch (error) {
        console.error("Failed to load ticket details", error);
      }
    };

    loadDetails();
  }, [ticket]);

  if (!ticket) return null;

  const handleDetailChange = (detail, value) => {
    setCollectedDetails((prev) => ({
      ...prev,
      [detail]: value,
    }));
  };

  const handleSave = async () => {
    try {
      setSaving(true);

      if (status !== ticket.status) {
        await updateTicketStatus(ticket.ticket_id, status);
      }

      if (note !== (ticket.officer_note || "")) {
        await updateOfficerNote(ticket.ticket_id, note);
      }

      await updateCollectedDetails(ticket.ticket_id, collectedDetails);

      onUpdated();
      onClose();
    } catch (error) {
      console.error("Failed to update ticket", error);
      alert("Failed to update ticket.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="details-backdrop">
      <div className="details-panel">
        <div className="details-header">
          <div>
            <h2>{ticket.ticket_id}</h2>
            <p className="muted">{ticket.category}</p>
          </div>
          <button onClick={onClose}>Close</button>
        </div>

        <div className="details-grid">
          <div>
            <span>Customer</span>
            <strong>{ticket.customer_name || "Not provided"}</strong>
          </div>
          <div>
            <span>Account Last 4</span>
            <strong>{ticket.account_last4 || "N/A"}</strong>
          </div>
          <div>
            <span>Phone</span>
            <strong>{ticket.phone || "N/A"}</strong>
          </div>
          <div>
            <span>Severity</span>
            <strong>{ticket.severity}</strong>
          </div>
          <div>
            <span>Risk Score</span>
            <strong>{ticket.risk_score}</strong>
          </div>
          <div>
            <span>Amount</span>
            <strong>₹{ticket.amount}</strong>
          </div>
        </div>

        <section>
          <h3>Complaint</h3>
          <p>{ticket.original_complaint}</p>
        </section>

        <section>
          <h3>Required Details to Collect</h3>

          <div className="detail-input-list">
            {ticket.missing_details?.map((detail, index) => (
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
        </section>

        <section>
          <h3>Recommended Action</h3>
          <p>{ticket.recommended_action}</p>
        </section>

        <section>
          <h3>Officer Summary</h3>
          <p>{ticket.officer_summary}</p>
        </section>

        <section>
          <h3>Update Ticket</h3>
          <div className="update-box">
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option value="Open">Open</option>
              <option value="In Review">In Review</option>
              <option value="Escalated">Escalated</option>
              <option value="Resolved">Resolved</option>
              <option value="Rejected">Rejected</option>
            </select>

            <textarea
              rows="3"
              placeholder="Officer note..."
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />

            <button onClick={handleSave} disabled={saving}>
              {saving ? "Saving..." : "Save Updates"}
            </button>
          </div>
        </section>

        <section>
          <h3>Alerts</h3>
          {alerts.length === 0 ? (
            <p className="muted">No alerts created for this ticket.</p>
          ) : (
            alerts.map((alert) => (
              <div className="log-card" key={alert.id}>
                <strong>{alert.alert_type}</strong>
                <p>Status: {alert.status}</p>
                <p>Recipient: {alert.recipient}</p>
              </div>
            ))
          )}
        </section>

        <section>
          <h3>Case Activity Timeline</h3>
          {auditLogs.length === 0 ? (
            <p className="muted">No case activity found.</p>
          ) : (
            auditLogs.map((log) => (
              <div className="log-card" key={log.id}>
                <strong>{log.action}</strong>
                <p>{log.details}</p>
                <small>{new Date(log.created_at).toLocaleString()}</small>
              </div>
            ))
          )}
        </section>
      </div>
    </div>
  );
}

export default TicketDetails;