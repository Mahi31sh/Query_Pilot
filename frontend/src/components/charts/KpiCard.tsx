import type { ChartSpec } from "@/lib/types";

const KpiCard = ({ chart }: { chart: ChartSpec }) => {
  const row = chart.data[0] ?? {};
  const value = chart.y_key ? row[chart.y_key] : Object.values(row)[0];

  return (
    <div className="bg-gradient-to-br from-brand-500 to-brand-700 text-white rounded-xl px-6 py-5 max-w-xs shadow-sm animate-slide-up">
      <p className="text-sm text-brand-100 mb-1">{chart.label ?? "Result"}</p>
      <p className="text-3xl font-bold">{String(value ?? "—")}</p>
    </div>
  );
};

export default KpiCard;