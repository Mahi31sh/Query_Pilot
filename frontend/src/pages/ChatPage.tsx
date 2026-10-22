import { useQueryChat } from "@/hooks/useQueryChat";
import ChatWindow from "@/components/chat/ChatWindow";
import QueryInput from "@/components/chat/QueryInput";

export default function ChatPage() {
  const { messages, sendQuestion, isLoading } = useQueryChat();

  return (
    <div className="h-full flex flex-col">
      <ChatWindow messages={messages} isLoading={isLoading} onSuggestionSelect={sendQuestion} />
      <QueryInput onSubmit={sendQuestion} disabled={isLoading} />
    </div>
  );
}