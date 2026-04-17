import { useState, useRef, useEffect, useCallback } from "react";
import { useTheme } from "@/hooks/useTheme";
import ChatHeader from "@/components/chat/ChatHeader";
import ChatBubble, { type Message } from "@/components/chat/ChatBubble";
import ChatInput from "@/components/chat/ChatInput";
import TypingIndicator from "@/components/chat/TypingIndicator";
import EmptyState from "@/components/chat/EmptyState";

const API_BASE = "http://localhost:8003";

const Index = () => {
  const { dark, toggle } = useTheme();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(
    () => localStorage.getItem("therapy_session_id")
  );
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping, scrollToBottom]);

  const handleSend = async (text: string) => {
    const userMsg: Message = { id: crypto.randomUUID(), role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, message: text }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

      const data = await res.json();

      if (!sessionId) {
        setSessionId(data.session_id);
        localStorage.setItem("therapy_session_id", data.session_id);
      }

      const botMsg: Message = { id: crypto.randomUUID(), role: "bot", content: data.reply };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const errMsg: Message = {
        id: crypto.randomUUID(),
        role: "bot",
        content: "I'm having trouble connecting right now. Please try again in a moment.",
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      <ChatHeader dark={dark} onToggle={toggle} />
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-4 py-6"
      >
        <div className="max-w-3xl mx-auto flex flex-col gap-3">
          {messages.length === 0 && !isTyping && <EmptyState />}
          {messages.map((msg) => (
            <ChatBubble key={msg.id} {...msg} />
          ))}
          {isTyping && <TypingIndicator />}
        </div>
      </div>
      <ChatInput onSend={handleSend} disabled={isTyping} />
    </div>
  );
};

export default Index;
