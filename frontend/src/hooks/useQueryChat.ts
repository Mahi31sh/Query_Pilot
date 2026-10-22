/**
 * Drives the chat page: sends questions to the backend via React Query's
 * useMutation, and maintains the running message list (user questions +
 * assistant results/errors) for rendering.
 */
import { useCallback, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { runQuery, extractErrorMessage } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export const useQueryChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const mutation = useMutation({
    mutationFn: (question: string) => runQuery(question),
  });

  const sendQuestion = useCallback(
    async (question: string) => {
      const trimmed = question.trim();
      if (!trimmed) return;

      setMessages((prev) => [...prev, { id: generateId(), role: "user", content: trimmed }]);

      try {
        const result = await mutation.mutateAsync(trimmed);
        setMessages((prev) => [...prev, { id: generateId(), role: "assistant", result }]);
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          { id: generateId(), role: "assistant-error", message: extractErrorMessage(err) },
        ]);
      }
    },
    [mutation]
  );

  return {
    messages,
    sendQuestion,
    isLoading: mutation.isPending,
  };
};