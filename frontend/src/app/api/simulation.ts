type Customer = {
  id: string;
  name: string;
};

type Scenario = {
  id: string;
  name: string;
};

type ScenarioRequest = {
  account_number: string;
  scenario_id: string;
};

type ManualTransactionRequest = {
  account_number: string;
  transaction_amount: number;
  transaction_currency: string;
  transaction_type: string;
  purpose?: string;
};

export async function getCustomers() {
  const { apiGet } = await import("@/app/api/client");
  return apiGet<Customer[]>("/api/v1/customers");
}

export async function getScenarios() {
  const { apiGet, unwrapData } = await import("@/app/api/client");
  const response = await apiGet<{
    success: boolean;
    data: { scenario_id: string; name: string; description: string }[];
  }>("/api/v1/simulate/scenarios");
  const scenarios = unwrapData(response);
  return scenarios.map((item) => ({ id: item.scenario_id, name: item.name }));
}

export async function runScenario(_payload: ScenarioRequest) {
  const { apiPost, unwrapData } = await import("@/app/api/client");
  const response = await apiPost(
    `/api/v1/simulate/scenario?account_number=${encodeURIComponent(_payload.account_number)}`,
    { scenario_id: _payload.scenario_id }
  );
  return unwrapData(response);
}

export async function createTransaction(_payload: ManualTransactionRequest) {
  const { apiPost } = await import("@/app/api/client");
  return apiPost("/api/v1/transactions", _payload);
}
