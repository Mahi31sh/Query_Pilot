import type { ChartSpec } from "@/lib/types";
import KpiCard from "./KpiCard";
import BarChartView from "./BarChartView";
import LineChartView from "./LineChartView";
import PieChartView from "./PieChartView";
import ResultTable from "@/components/data/ResultTable";

const ChartRenderer = ({ chart, columns }: { chart: ChartSpec; columns: string[] }) => {
  switch (chart.chart_type) {
    case "kpi":
      return <KpiCard chart={chart} />;
    case "bar":
      return <BarChartView chart={chart} />;
    case "line":
      return <LineChartView chart={chart} />;
    case "pie":
      return <PieChartView chart={chart} />;
    case "scatter":
      return <BarChartView chart={chart} />; // scatter falls back to bar rendering for simplicity
    case "table":
    default:
      return <ResultTable columns={columns} rows={chart.data} />;
  }
};

export default ChartRenderer;