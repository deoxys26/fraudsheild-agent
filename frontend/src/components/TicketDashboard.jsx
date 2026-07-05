import { useEffect, useState } from "react";
import { getTickets } from "../api/api";
import TicketCard from "./TicketCard";
import TicketDetails from "./TicketDetails";

function TicketDashboard({ refreshKey }) {
  const [tickets, setTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);

  const [filters, setFilters] = useState({
    status: "",
    severity: "",
    category: "",
  });

  const [loading, setLoading] = useState(false);

  const fetchTickets = async () => {
    try {
      setLoading(true);

      const activeFilters = {};
      Object.entries(filters).forEach(([key, value]) => {
        if (value) activeFilters[key] = value;
      });

      const data = await getTickets(activeFilters);
      setTickets(data);
    } catch (error) {
      console.error("Failed to fetch tickets", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, [refreshKey]);

  const handleFilterChange = (e) => {
    setFilters((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleTicketUpdated = async () => {
    await fetchTickets();
  };

  return (
    <div className="panel dashboard">
      <div className="dashboard-header">
        <div>
          <h2>Ticket Dashboard</h2>
          <p className="muted">View saved PostgreSQL fraud tickets.</p>
        </div>
        <button onClick={fetchTickets}>Refresh</button>
      </div>

      <div className="filters">
        <select name="status" value={filters.status} onChange={handleFilterChange}>
          <option value="">All Status</option>
          <option value="Open">Open</option>
          <option value="In Review">In Review</option>
          <option value="Escalated">Escalated</option>
          <option value="Resolved">Resolved</option>
          <option value="Rejected">Rejected</option>
        </select>

        <select name="severity" value={filters.severity} onChange={handleFilterChange}>
          <option value="">All Severity</option>
          <option value="Critical">Critical</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>

        <select name="category" value={filters.category} onChange={handleFilterChange}>
          <option value="">All Categories</option>
          <option value="Phishing Fraud">Phishing Fraud</option>
          <option value="Unauthorized UPI Transaction">Unauthorized UPI Transaction</option>
          <option value="ATM Cash Not Dispensed">ATM Cash Not Dispensed</option>
          <option value="Card Fraud">Card Fraud</option>
          <option value="Wrong Beneficiary Transfer">Wrong Beneficiary Transfer</option>
          <option value="Suspicious Account Activity">Suspicious Account Activity</option>
        </select>

        <button onClick={fetchTickets}>Apply</button>
      </div>

      {loading ? (
        <p className="muted">Loading tickets...</p>
      ) : (
        <div className="ticket-list">
          {tickets.length === 0 ? (
            <p className="muted">No tickets found.</p>
          ) : (
            tickets.map((ticket) => (
              <div
                key={ticket.ticket_id}
                onClick={() => setSelectedTicket(ticket)}
              >
                <TicketCard ticket={ticket} />
              </div>
            ))
          )}
        </div>
      )}

      {selectedTicket && (
        <TicketDetails
          ticket={selectedTicket}
          onClose={() => setSelectedTicket(null)}
          onUpdated={handleTicketUpdated}
        />
      )}
    </div>
  );
}

export default TicketDashboard;