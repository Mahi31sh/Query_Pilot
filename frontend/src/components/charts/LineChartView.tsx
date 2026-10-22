import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import type { ChartSpec } from "@/lib/types";

const LineChartView = ({ chart }: { chart: ChartSpec }) => {
  if (!chart.x_key || !chart.y_key) return null;

  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={chart.data}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-800" />
        <XAxis dataKey={chart.x_key} tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />
        <Line type="monotone" dataKey={chart.y_key} stroke="#4f46e5" strokeWidth={2} dot={{ r: 3 }} />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default LineChartView;