import { useState } from "react";
import { Code2 } from "lucide-react";
import type { ChatMessage } from "@/lib/types";
import ChartRenderer from "@/components/charts/ChartRenderer";
import CsvDownloadButton from "@/components/data/CsvDownloadButton";
import ErrorBanner from "@/components/ui/ErrorBanner";

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const [showSql, setShowSql] = useState(false);

  if (message.role === "user") {
    return (
      <div className="flex justify-end animate-slide-up">
        <div className="bg-brand-600 text-white rounded-2xl rounded-tr-sm px-4 py-2.5 max-w-lg text-sm">
          {message.content}
        </div>
      </div>
    );
  }

  if (message.role === "assistant-error") {
    return (
      <div className="flex justify-start animate-slide-up max-w-lg">
        <ErrorBanner message={message.message} />
      </div>
    );
  }

  const { result } = message;

  return (
    <div className="flex justify-start animate-slide-up">
      <div className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl rounded-tl-sm px-5 py-4 max-w-2xl w-full space-y-3">
        <p className="text-sm text-gray-700 dark:text-gray-300">{result.explanation}</p>

        <ChartRenderer chart={result.chart} columns={result.columns} />

        <div className="flex items-center justify-between pt-1">
          <button
            onClick={() => setShowSql((s) => !s)}
            className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 hover:text-brand-600 dark:hover:text-brand-400"
          >
            <Code2 size={13} />
            {showSql ? "Hide SQL" : "Show SQL"}
          </button>
          <CsvDownloadButton columns={result.columns} rows={result.rows} />
        </div>

        {showSql && (
          <pre className="bg-gray-900 dark:bg-black text-gray-100 text-xs rounded-lg p-3 overflow-x-auto">
            <code>{result.generated_sql}</code>
          </pre>
        )}

        <p className="text-[11px] text-gray-400 dark:text-gray-600">
          {result.row_count} rows · {result.execution_time_ms.toFixed(0)}ms
          {result.retry_count > 0 && ` · self-corrected ${result.retry_count}x`}
        </p>
      </div>
    </div>
  );
}