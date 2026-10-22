import type { QueryHistoryItem } from "@/lib/types";
import { useState } from "react";
import { useHistory } from "@/hooks/useHistory";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import ErrorBanner from "@/components/ui/ErrorBanner";
import { extractErrorMessage } from "@/lib/api";
import { CheckCircle2, XCircle, Code2 } from "lucide-react";

export default function HistoryPage() {
  const { data: history, isLoading, error } = useHistory(50, 0);
  const historyItems: QueryHistoryItem[] = history ?? [];
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <LoadingSpinner label="Loading history..." />
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

  if (historyItems.length === 0) {
    return <p className="p-6 text-sm text-gray-500 dark:text-gray-400">No queries yet.</p>;
  }

  return (
    <div className="p-6 space-y-3 max-w-3xl">
      <h1 className="text-xl font-semibold mb-3">Query History</h1>
      {historyItems.map((item) => (
        <div
          key={item.id}
          className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-4"
        >
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-start gap-2">
              {item.success ? (
                <CheckCircle2 size={16} className="text-green-600 mt-0.5 shrink-0" />
              ) : (
                <XCircle size={16} className="text-red-600 mt-0.5 shrink-0" />
              )}
              <div>
                <p className="text-sm font-medium">{item.question}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                  {new Date(item.created_at).toLocaleString()}
                  {item.row_count !== null && ` · ${item.row_count} rows`}
                  {item.retry_count > 0 && ` · ${item.retry_count} retries`}
                </p>
              </div>
            </div>
            {item.success && (
              <button
                onClick={() => setExpandedId(expandedId === item.id ? null : item.id)}
                className="text-xs text-gray-500 dark:text-gray-400 hover:text-brand-600 flex items-center gap-1 shrink-0"
              >
                <Code2 size={13} />
                SQL
              </button>
            )}
          </div>

          {!item.success && item.error_message && (
            <p className="text-xs text-red-600 dark:text-red-400 mt-2 ml-6">{item.error_message}</p>
          )}

          {expandedId === item.id && (
            <pre className="bg-gray-900 dark:bg-black text-gray-100 text-xs rounded-lg p-3 overflow-x-auto mt-3">
              <code>{item.generated_sql}</code>
            </pre>
          )}
        </div>
      ))}
    </div>
  );
}