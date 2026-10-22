import { Download } from "lucide-react";

interface CsvDownloadButtonProps {
  columns: string[];
  rows: Record<string, unknown>[];
  filename?: string;
}

function toCsv(columns: string[], rows: Record<string, unknown>[]): string {
  const escape = (val: unknown) => `"${String(val ?? "").replace(/"/g, '""')}"`;
  const header = columns.map(escape).join(",");
  const body = rows.map((row) => columns.map((col) => escape(row[col])).join(",")).join("\n");
  return `${header}\n${body}`;
}

const CsvDownloadButton = ({ columns, rows, filename = "query-results.csv" }: CsvDownloadButtonProps) => {
  function handleDownload() {
    const csv = toCsv(columns, rows);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  }

  if (rows.length === 0) return null;

  return (
    <button
      onClick={handleDownload}
      className="flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-md border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:border-brand-500 hover:text-brand-600 transition-colors"
    >
      <Download size={13} />
      Export CSV
    </button>
  );
};

export default CsvDownloadButton;