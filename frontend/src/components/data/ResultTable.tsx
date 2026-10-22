interface ResultTableProps {
  columns: string[];
  rows: Record<string, unknown>[];
}

const ResultTable = ({ columns, rows }: ResultTableProps) => {
  if (rows.length === 0) {
    return <p className="text-sm text-gray-500 dark:text-gray-400 py-4">No rows returned.</p>;
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-800">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50 dark:bg-gray-900">
          <tr>
            {columns.map((col) => (
              <th key={col} className="text-left font-medium px-4 py-2.5 text-gray-600 dark:text-gray-300">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className="border-t border-gray-100 dark:border-gray-800">
              {columns.map((col) => (
                <td key={col} className="px-4 py-2.5 text-gray-800 dark:text-gray-200">
                  {String(row[col] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResultTable;