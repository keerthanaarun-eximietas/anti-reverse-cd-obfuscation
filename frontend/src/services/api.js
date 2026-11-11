
const API_BASE_URL = "http://127.0.0.1:5000/api";

async function request(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function getTransactions() {
  return request("/transactions");
}

export function getSummary() {
  return request("/reports/summary");
}

export function checkHealth() {
  return request("/health");
}


export async function createTransaction(transaction) {
  const response = await fetch(`${API_BASE_URL}/transactions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(transaction),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to submit transaction");
  }

  return data;
}
