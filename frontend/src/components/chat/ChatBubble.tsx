import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";

export interface Message {
  id: string;
  role: "user" | "bot";
  content: string;
}

const ChatBubble = ({ role, content }: Message) => {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`flex ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`max-w-[80%] sm:max-w-[70%] px-4 py-3 rounded-2xl text-[0.935rem] leading-relaxed ${
          isUser
            ? "bg-chat-user text-chat-user-foreground rounded-br-md"
            : "bg-chat-bot text-chat-bot-foreground rounded-bl-md"
        }`}
      >
        <div className="prose prose-sm dark:prose-invert max-w-none [&>p]:m-0">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </motion.div>
  );
};

export default ChatBubble;
