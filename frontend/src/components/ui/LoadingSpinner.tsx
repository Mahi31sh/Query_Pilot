import { Loader2 } from "lucide-react";
import clsx from "clsx";

interface LoadingSpinnerProps {
  size?: number;
  label?: string;
  className?: string;
}

export default function LoadingSpinner({ size = 20, label, className }: LoadingSpinnerProps) {
  return (
    <div className={clsx("flex items-center gap-2 text-gray-500 dark:text-gray-400", className)}>
      <Loader2 size={size} className="animate-spin" />
      {label && <span className="text-sm">{label}</span>}
    </div>
  );
}