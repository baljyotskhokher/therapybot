import { Heart } from "lucide-react";
import { motion } from "framer-motion";

const EmptyState = () => (
  <motion.div
    initial={{ opacity: 0, scale: 0.95 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ duration: 0.5, ease: "easeOut" }}
    className="flex flex-col items-center justify-center gap-4 text-center px-6 py-20"
  >
    <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10">
      <Heart size={28} className="text-primary" />
    </div>
    <div>
      <p className="text-foreground font-medium text-lg">Start your conversation</p>
      <p className="text-muted-foreground text-sm mt-1">I'm here to listen.</p>
    </div>
  </motion.div>
);

export default EmptyState;
