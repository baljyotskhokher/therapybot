import ThemeToggle from "./ThemeToggle";
import { Heart } from "lucide-react";

interface ChatHeaderProps {
  dark: boolean;
  onToggle: () => void;
}

const ChatHeader = ({ dark, onToggle }: ChatHeaderProps) => (
  <header className="flex items-center justify-between px-6 py-4 border-b border-border bg-card/80 backdrop-blur-sm">
    <div className="flex items-center gap-2.5">
      <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-primary/10">
        <Heart size={18} className="text-primary" />
      </div>
      <h1 className="text-lg font-semibold text-foreground tracking-tight">Therapy Bot</h1>
    </div>
    <ThemeToggle dark={dark} onToggle={onToggle} />
  </header>
);

export default ChatHeader;
