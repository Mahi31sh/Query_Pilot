import { useEffect, useRef } from "react";
import type { ChatMessage } from "@/lib/types";
import MessageBubble from "./MessageBubble";
import SuggestedQuestions from "./SuggestedQuestions";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

interface ChatWindowProps {
  messages: ChatMessage[];
  isLoading: boolean;
  onSuggestionSelect: (question: string) => void;
}

export default function ChatWindow({ messages, isLoading, onSuggestionSelect }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center gap-6 px-6 text-center">
        <div>
          <h2 className="text-xl font-semibold mb-1.5">Ask your data anything</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            QueryPilot turns plain English into SQL, runs it, and visualizes the result.
          </p>
        </div>
        <SuggestedQuestions onSelect={onSuggestionSelect} />
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto scrollbar-thin px-6 py-6 space-y-4">
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}
      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl rounded-tl-sm px-5 py-3">
            <LoadingSpinner label="Generating SQL and running query..." />
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}