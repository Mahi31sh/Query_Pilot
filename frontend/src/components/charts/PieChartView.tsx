import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import type { ChartSpec } from "@/lib/types";

const COLORS = ["#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe", "#4338ca", "#4f46e5", "#312e81", "#e0e7ff"];

const PieChartView = ({ chart }: { chart: ChartSpec }) => {
  if (!chart.x_key || !chart.y_key) return null;

  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={chart.data}
          dataKey={chart.y_key}
          nameKey={chart.x_key}
          cx="50%"
          cy="50%"
          outerRadius={90}
          label
        >
          {chart.data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default PieChartView;