function TicketCard({ ticket }) {
  return (
    <div className="ticket-card">
      <div className="ticket-top">
        <strong>{ticket.ticket_id}</strong>
        <span>{ticket.status}</span>
      </div>

      <p className="ticket-category">{ticket.category}</p>

      <div className="ticket-customer">
        <strong>{ticket.customer_name || "No customer name"}</strong>
        <span>Acc: {ticket.account_last4 || "N/A"}</span>
        <span>Phone: {ticket.phone || "N/A"}</span>
      </div>

      <div className="ticket-meta">
        <span>Severity: {ticket.severity}</span>
        <span>Risk: {ticket.risk_score}</span>
        <span>₹{ticket.amount}</span>
      </div>

      <p className="ticket-summary">{ticket.officer_summary}</p>

      <div className="ticket-footer">
        <span>{ticket.officer_note ? "Officer note added" : "No officer note"}</span>
        <span>{new Date(ticket.created_at).toLocaleString()}</span>
      </div>
    </div>
  );
}

export default TicketCard;