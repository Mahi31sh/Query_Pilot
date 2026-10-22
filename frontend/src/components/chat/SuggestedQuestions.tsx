interface SuggestedQuestionsProps {
  onSelect: (question: string) => void;
}

const SUGGESTIONS = [
  "What is the total revenue from completed orders?",
  "Show me revenue by product category",
  "Which 5 customers have spent the most?",
  "How many orders were placed each month?",
  "What is the average order value by country?",
];

export default function SuggestedQuestions({ onSelect }: SuggestedQuestionsProps) {
  return (
    <div className="flex flex-wrap gap-2 justify-center max-w-2xl">
      {SUGGESTIONS.map((q) => (
        <button
          key={q}
          onClick={() => onSelect(q)}
          className="text-sm px-3.5 py-2 rounded-full border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:border-brand-500 hover:text-brand-600 dark:hover:text-brand-400 transition-colors"
        >
          {q}
        </button>
      ))}
    </div>
  );
}