import { useEffect, useMemo, useState } from "react";
import { createTransaction, getScenarios, runScenario } from "@/app/api/simulation";
import { listCustomers } from "@/app/api/customers";
import { listAccountsByCustomer } from "@/app/api/accounts";

type TabKey = "scenario" | "manual";

type FieldErrors = {
  customer?: string;
  account?: string;
  scenario?: string;
  amount?: string;
  currency?: string;
  transactionType?: string;
};

export default function TransactionDemoPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("scenario");
  const [customers, setCustomers] = useState<{ id: string; name: string }[]>([]);
  const [accounts, setAccounts] = useState<{ id: string; label: string }[]>([]);
  const [scenarios, setScenarios] = useState<{ id: string; name: string }[]>([]);
  const [customerId, setCustomerId] = useState("");
  const [accountId, setAccountId] = useState("");
  const [scenarioId, setScenarioId] = useState("");
  const [amount, setAmount] = useState("");
  const [currency, setCurrency] = useState("USD");
  const [transactionType, setTransactionType] = useState("deposit");
  const [purpose, setPurpose] = useState("");
  const [errors, setErrors] = useState<FieldErrors>({});
  const [status, setStatus] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    listCustomers().then((data) => {
      const mapped = data.items.map((item) => ({
        id: item.customer_id,
        name: item.full_name
      }));
      setCustomers(mapped);
    });
    getScenarios().then(setScenarios);
  }, []);

  useEffect(() => {
    if (!customerId) {
      setAccounts([]);
      setAccountId("");
      return;
    }
    listAccountsByCustomer(customerId).then((data) => {
      const mapped = data.items.map((item) => ({
        id: item.account_number,
        label: `${item.account_number} • ${item.account_status}`
      }));
      setAccounts(mapped);
      if (mapped.length > 0) {
        setAccountId(mapped[0].id);
      }
    });
  }, [customerId]);

  useEffect(() => {
    setStatus("");
    setErrors({});
  }, [activeTab]);

  const activeCustomer = useMemo(
    () => customers.find((customer) => customer.id === customerId),
    [customers, customerId]
  );

  const validateScenario = () => {
    const nextErrors: FieldErrors = {};
    if (!customerId) {
      nextErrors.customer = "Select a customer.";
    }
    if (!accountId) {
      nextErrors.account = "Select an account.";
    }
    if (!scenarioId) {
      nextErrors.scenario = "Select a scenario.";
    }
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const validateManual = () => {
    const nextErrors: FieldErrors = {};
    if (!customerId) {
      nextErrors.customer = "Select a customer.";
    }
    if (!accountId) {
      nextErrors.account = "Select an account.";
    }
    if (!amount || Number.isNaN(Number(amount))) {
      nextErrors.amount = "Enter a valid amount.";
    }
    if (!currency) {
      nextErrors.currency = "Select a currency.";
    }
    if (!transactionType) {
      nextErrors.transactionType = "Select a transaction type.";
    }
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleScenarioSubmit = async () => {
    if (!validateScenario()) {
      return;
    }
    setIsSubmitting(true);
    setStatus("");
    try {
      await runScenario({ account_number: accountId, scenario_id: scenarioId });
      setStatus(`Scenario triggered for ${activeCustomer?.name ?? "customer"}.`);
    } catch (error) {
      setStatus("Unable to run scenario. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleManualSubmit = async () => {
    if (!validateManual()) {
      return;
    }
    setIsSubmitting(true);
    setStatus("");
    try {
      await createTransaction({
        account_number: accountId,
        transaction_amount: Number(amount),
        transaction_currency: currency,
        transaction_type: transactionType,
        purpose
      });
      setStatus("Transaction submitted for monitoring.");
    } catch (error) {
      setStatus("Unable to submit transaction. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Transaction Simulation</h2>
        <p className="mt-2 text-sm text-text-muted">
          Public simulation for testing scenarios and manual transactions without login.
        </p>
      </div>

      <div className="inline-flex rounded-full border border-border bg-surface-secondary p-1">
        {(["scenario", "manual"] as TabKey[]).map((tab) => (
          <button
            key={tab}
            type="button"
            onClick={() => setActiveTab(tab)}
            className={[
              "rounded-full px-4 py-2 text-sm font-semibold transition",
              activeTab === tab
                ? "bg-brand text-brand-foreground shadow-soft"
                : "text-text-muted hover:text-brand"
            ].join(" ")}
          >
            {tab === "scenario" ? "Scenario" : "Manual"}
          </button>
        ))}
      </div>

      <div className="rounded-2xl border border-border bg-surface-secondary p-6">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium text-text" htmlFor="customer">
              Customer
            </label>
            <select
              id="customer"
              value={customerId}
              onChange={(event) => setCustomerId(event.target.value)}
              className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text"
            >
              <option value="">Select customer</option>
              {customers.map((customer) => (
                <option key={customer.id} value={customer.id}>
                  {customer.name}
                </option>
              ))}
            </select>
            {errors.customer ? (
              <p className="text-xs text-red-500">{errors.customer}</p>
            ) : null}
          </div>

          {activeTab === "scenario" ? (
            <>
              <div className="space-y-2">
                <label className="text-sm font-medium text-text" htmlFor="accountScenario">
                  Account
                </label>
                <select
                  id="accountScenario"
                  value={accountId}
                  onChange={(event) => setAccountId(event.target.value)}
                  className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text"
                >
                  <option value="">Select account</option>
                  {accounts.map((account) => (
                    <option key={account.id} value={account.id}>
                      {account.label}
                    </option>
                  ))}
                </select>
                {errors.account ? (
                  <p className="text-xs text-red-500">{errors.account}</p>
                ) : null}
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-text" htmlFor="scenario">
                  Simulation scenario
                </label>
                <select
                  id="scenario"
                  value={scenarioId}
                  onChange={(event) => setScenarioId(event.target.value)}
                  className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text"
                >
                  <option value="">Select scenario</option>
                  {scenarios.map((scenario) => (
                    <option key={scenario.id} value={scenario.id}>
                      {scenario.name}
                    </option>
                  ))}
                </select>
                {errors.scenario ? (
                  <p className="text-xs text-red-500">{errors.scenario}</p>
                ) : null}
              </div>
            </>
          ) : (
            <>
              <div className="space-y-2">
                <label className="text-sm font-medium text-text" htmlFor="account">
                  Account
                </label>
                <select
                  id="account"
                  value={accountId}
                  onChange={(event) => setAccountId(event.target.value)}
                  className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text"
                >
                  <option value="">Select account</option>
                  {accounts.map((account) => (
                    <option key={account.id} value={account.id}>
                      {account.label}
                    </option>
                  ))}
                </select>
                {errors.account ? (
                  <p className="text-xs text-red-500">{errors.account}</p>
                ) : null}
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-text" htmlFor="amount">
                  Amount
                </label>
                <input
                  id="amount"
                  type="number"
                  value={amount}
                  onChange={(event) => setAmount(event.target.value)}
                  className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text"
                  placeholder="5000"
                />
                {errors.amount ? (
                  <p className="text-xs text-red-500">{errors.amount}</p>
                ) : null}
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-text" htmlFor="currency">
                  Currency
                </label>
                <select
                  id="currency"
                  value={currency}
                  onChange={(event) => setCurrency(event.target.value)}
                  className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text"
                >
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                  <option value="GBP">GBP</option>
                </select>
                {errors.currency ? (
                  <p className="text-xs text-red-500">{errors.currency}</p>
                ) : null}
              </div>
              <div className="space-y-2 sm:col-span-2">
                <label className="text-sm font-medium text-text" htmlFor="transactionType">
                  Transaction type
                </label>
                <select
                  id="transactionType"
                  value={transactionType}
                  onChange={(event) => setTransactionType(event.target.value)}
                  className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text"
                >
                  <option value="deposit">Deposit</option>
                  <option value="withdrawal">Withdrawal</option>
                  <option value="trade-buy">Trade Buy</option>
                  <option value="trade-sell">Trade Sell</option>
                </select>
                {errors.transactionType ? (
                  <p className="text-xs text-red-500">{errors.transactionType}</p>
                ) : null}
              </div>
              <div className="space-y-2 sm:col-span-2">
                <label className="text-sm font-medium text-text" htmlFor="purpose">
                  Purpose (optional)
                </label>
                <input
                  id="purpose"
                  type="text"
                  value={purpose}
                  onChange={(event) => setPurpose(event.target.value)}
                  className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text"
                  placeholder="Funding trading account"
                />
              </div>
            </>
          )}
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-3">
          {activeTab === "scenario" ? (
            <button
              type="button"
              onClick={handleScenarioSubmit}
              disabled={isSubmitting}
              className="rounded-full bg-brand px-5 py-2.5 text-sm font-semibold text-brand-foreground shadow-soft disabled:opacity-70"
            >
              {isSubmitting ? "Running..." : "Run Scenario"}
            </button>
          ) : (
            <button
              type="button"
              onClick={handleManualSubmit}
              disabled={isSubmitting}
              className="rounded-full bg-brand px-5 py-2.5 text-sm font-semibold text-brand-foreground shadow-soft disabled:opacity-70"
            >
              {isSubmitting ? "Submitting..." : "Submit Transaction"}
            </button>
          )}
          <p className="text-sm text-text-muted">
            Simulation flows call the backend endpoints.
          </p>
        </div>

        {status ? (
          <div className="mt-4 rounded-xl border border-border bg-surface px-4 py-3 text-sm">
            {status}
          </div>
        ) : null}
      </div>
    </div>
  );
}
