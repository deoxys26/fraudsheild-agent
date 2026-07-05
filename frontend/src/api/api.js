import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const analyzeComplaint = async (payload) => {
  const response = await axios.post(
    `${API_BASE_URL}/api/complaints/analyze`,
    payload
  );
  return response.data;
};

export const getTickets = async (filters = {}) => {
  const response = await axios.get(`${API_BASE_URL}/api/tickets/`, {
    params: filters,
  });
  return response.data;
};

export const updateTicketStatus = async (ticketId, status) => {
  const response = await axios.patch(
    `${API_BASE_URL}/api/tickets/${ticketId}/status`,
    { status }
  );
  return response.data;
};

export const updateOfficerNote = async (ticketId, note) => {
  const response = await axios.patch(
    `${API_BASE_URL}/api/tickets/${ticketId}/note`,
    { note }
  );
  return response.data;
};

export const getTicketAlerts = async (ticketId) => {
  const response = await axios.get(
    `${API_BASE_URL}/api/tickets/${ticketId}/alerts`
  );
  return response.data;
};

export const getTicketAuditLogs = async (ticketId) => {
  const response = await axios.get(
    `${API_BASE_URL}/api/tickets/${ticketId}/audit-logs`
  );
  return response.data;
};
export const updateCollectedDetails = async (ticketId, collectedDetails) => {
  const response = await axios.patch(
    `${API_BASE_URL}/api/tickets/${ticketId}/details`,
    { collected_details: collectedDetails }
  );
  return response.data;
};