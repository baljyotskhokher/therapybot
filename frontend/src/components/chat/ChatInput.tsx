import { useState, useRef } from "react";
import { SendHorizontal, Mic } from "lucide-react";

interface ChatInputProps {
  onSend: (text: string) => void;
  disabled?: boolean;
}

const ChatInput = ({ onSend, disabled }: ChatInputProps) => {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    inputRef.current?.focus();
  };

  return (
    <div className="px-4 py-4 border-t border-border bg-card/80 backdrop-blur-sm">
      <div className="flex items-center gap-2 max-w-3xl mx-auto">
        <div className="flex-1 flex items-center bg-secondary rounded-xl px-4 py-2.5 gap-2 focus-within:ring-2 focus-within:ring-ring/30 transition-shadow">
          <input
            ref={inputRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            placeholder="How are you feeling today?"
            disabled={disabled}
            className="flex-1 bg-transparent text-foreground placeholder:text-muted-foreground text-sm outline-none"
          />
          <button
            className="text-muted-foreground hover:text-foreground transition-colors"
            aria-label="Voice input (coming soon)"
            tabIndex={-1}
          >
            <Mic size={18} />
          </button>
        </div>
        <button
          onClick={handleSubmit}
          disabled={disabled || !value.trim()}
          className="flex items-center justify-center w-10 h-10 rounded-xl bg-primary text-primary-foreground hover:opacity-90 disabled:opacity-40 transition-all duration-150 active:scale-95"
          aria-label="Send message"
        >
          <SendHorizontal size={18} />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
