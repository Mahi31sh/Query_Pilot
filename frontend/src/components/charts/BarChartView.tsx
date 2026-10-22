import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import type { ChartSpec } from "@/lib/types";

const BarChartView = ({ chart }: { chart: ChartSpec }) => {
  if (!chart.x_key || !chart.y_key) return null;

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chart.data}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-800" />
        <XAxis dataKey={chart.x_key} tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />
        <Bar dataKey={chart.y_key} fill="#6366f1" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default BarChartView;