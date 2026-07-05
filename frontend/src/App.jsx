import { useState } from "react";
import ComplaintForm from "./components/ComplaintForm";
import ResultCard from "./components/ResultCard";
import TicketDashboard from "./components/TicketDashboard";
import "./index.css";

function App() {
  const [activePortal, setActivePortal] = useState("customer");
  const [result, setResult] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleTicketCreated = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">Agentic AI Banking Prototype</p>
          <h1>FraudShield Agent</h1>
          <p>
            A fraud complaint triage system with a customer complaint portal and
            an internal officer dashboard for risk scoring, escalation, alerts,
            and case tracking.
          </p>
        </div>

        <div className="hero-card">
          <span>System</span>
          <strong>Customer Portal + Officer Dashboard</strong>
          <small>FastAPI + PostgreSQL + Gemini</small>
        </div>
      </header>

      <div className="portal-tabs">
        <button
          className={activePortal === "customer" ? "active-tab" : ""}
          onClick={() => setActivePortal("customer")}
        >
          Customer Portal
        </button>

        <button
          className={activePortal === "officer" ? "active-tab" : ""}
          onClick={() => setActivePortal("officer")}
        >
          Officer Dashboard
        </button>
      </div>

      {activePortal === "customer" ? (
        <main className="customer-layout">
          <ComplaintForm
            onResult={setResult}
            onTicketCreated={handleTicketCreated}
          />
          <ResultCard result={result} />
        </main>
      ) : (
        <main className="officer-layout">
          <TicketDashboard refreshKey={refreshKey} />
        </main>
      )}
    </div>
  );
}

export default App;