import { Moon, Sun } from "lucide-react";
import { motion } from "framer-motion";

interface ThemeToggleProps {
  dark: boolean;
  onToggle: () => void;
}

const ThemeToggle = ({ dark, onToggle }: ThemeToggleProps) => (
  <button
    onClick={onToggle}
    className="relative flex items-center justify-center w-10 h-10 rounded-full bg-secondary text-secondary-foreground hover:bg-accent transition-colors duration-200"
    aria-label="Toggle theme"
  >
    <motion.div
      key={dark ? "moon" : "sun"}
      initial={{ rotate: -90, opacity: 0 }}
      animate={{ rotate: 0, opacity: 1 }}
      exit={{ rotate: 90, opacity: 0 }}
      transition={{ duration: 0.2 }}
    >
      {dark ? <Moon size={18} /> : <Sun size={18} />}
    </motion.div>
  </button>
);

export default ThemeToggle;
