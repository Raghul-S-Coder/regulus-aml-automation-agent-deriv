import { useMemo, useState } from "react";
import { EmptyState, ErrorState, LoadingState } from "@/app/components/States";
import { listTransactions } from "@/app/api/transactions";
import { useApi } from "@/app/hooks/useApi";

type TransactionRow = {
  id: string;
  account: string;
  type: string;
  amount: string;
  status: "pending" | "completed" | "held";
  date: string;
};

const statusStyle = (status: TransactionRow["status"]) =>
  ({
    completed: "bg-brand/10 text-brand",
    pending: "bg-amber-500/10 text-amber-600",
    held: "bg-rose-500/10 text-rose-600"
  })[status];

export default function TransactionsPage() {
  const [status, setStatus] = useState("all");
  const [type, setType] = useState("all");
  const [query, setQuery] = useState("");

  const { data, error, loading } = useApi(
    () =>
      listTransactions({
        page: 1,
        page_size: 50,
        transaction_status: status === "all" ? undefined : status,
        transaction_type:
          type === "all" || type === "trade"
            ? undefined
            : type
      }),
    [status, type]
  );

  const rows: TransactionRow[] = (data?.items ?? []).map((item) => ({
    id: item.transaction_id,
    account: item.account_number,
    type: item.transaction_type.replace("-", " "),
    amount: `${item.transaction_currency} ${item.transaction_amount.toFixed(2)}`,
    status: item.transaction_status as TransactionRow["status"],
    date: new Date(item.transaction_date).toLocaleString()
  }));

  const filtered = useMemo(() => {
    return rows.filter((row) => {
      const statusMatch = status === "all" || row.status === status;
      const typeMatch =
        type === "all" || row.type.toLowerCase().includes(type.replace("-", " "));
      const queryMatch =
        !query ||
        row.account.toLowerCase().includes(query.toLowerCase()) ||
        row.id.toLowerCase().includes(query.toLowerCase());
      return statusMatch && typeMatch && queryMatch;
    });
  }, [rows, status, type, query]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Transactions</h2>
        <p className="mt-2 text-sm text-text-muted">
          Filter and review transactions in real time.
        </p>
      </div>

      <div className="grid gap-3 rounded-2xl border border-border bg-surface-secondary p-4 sm:grid-cols-3">
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-text-muted">
            Status
          </label>
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value)}
            className="mt-2 w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm"
          >
            <option value="all">All</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
            <option value="held">Held</option>
          </select>
        </div>
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-text-muted">
            Type
          </label>
          <select
            value={type}
            onChange={(event) => setType(event.target.value)}
            className="mt-2 w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm"
          >
            <option value="all">All</option>
            <option value="deposit">Deposit</option>
            <option value="withdrawal">Withdrawal</option>
            <option value="trade-buy">Trade Buy</option>
            <option value="trade-sell">Trade Sell</option>
          </select>
        </div>
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-text-muted">
            Search
          </label>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Customer or TXN ID"
            className="mt-2 w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm"
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-border bg-surface-secondary">
        {loading ? (
          <div className="p-6">
            <LoadingState title="Loading transactions" />
          </div>
        ) : error ? (
          <div className="p-6">
            <ErrorState title="Unable to load transactions" message={error} />
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-6">
            <EmptyState title="No transactions found" message="Adjust your filters to see results." />
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="bg-surface-secondary/80 text-xs uppercase tracking-[0.2em] text-text-muted">
              <tr>
                <th className="px-4 py-3">Transaction ID</th>
                <th className="px-4 py-3">Account</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Amount</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Date</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row) => (
                <tr key={row.id} className="border-t border-border">
                  <td className="px-4 py-3 font-medium text-text">{row.id}</td>
                  <td className="px-4 py-3 text-text-muted">{row.account}</td>
                  <td className="px-4 py-3 text-text-muted">{row.type}</td>
                  <td className="px-4 py-3 text-text">{row.amount}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-full px-2 py-1 text-xs font-semibold ${statusStyle(
                        row.status
                      )}`}
                    >
                      {row.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-text-muted">{row.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
