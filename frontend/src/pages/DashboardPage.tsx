import type { QueryHistoryItem } from "@/lib/types";
import { useHistory } from "@/hooks/useHistory";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import ErrorBanner from "@/components/ui/ErrorBanner";
import { extractErrorMessage } from "@/lib/api";

export default function DashboardPage() {
  const { data: history, isLoading, error } = useHistory(200, 0);
  const historyItems: QueryHistoryItem[] = history ?? [];

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <LoadingSpinner label="Loading dashboard..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <ErrorBanner message={extractErrorMessage(error)} />
      </div>
    );
  }

  const total = historyItems.length;
  const successful = historyItems.filter((item) => item.success).length;
  const successRate = total > 0 ? ((successful / total) * 100).toFixed(0) : "0";
  const avgRetries =
    total > 0 ? (historyItems.reduce((sum, item) => sum + item.retry_count, 0) / total).toFixed(1) : "0";
  const totalRows = historyItems.reduce((sum, item) => sum + (item.row_count ?? 0), 0);

  const stats = [
    { label: "Total Queries", value: total },
    { label: "Success Rate", value: `${successRate}%` },
    { label: "Avg Self-Correction Retries", value: avgRetries },
    { label: "Total Rows Returned", value: totalRows },
  ];

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-5">Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div
            key={s.label}
            className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-4"
          >
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{s.label}</p>
            <p className="text-2xl font-semibold">{s.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}