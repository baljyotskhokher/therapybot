const TypingIndicator = () => (
  <div className="flex justify-start">
    <div className="bg-chat-bot px-4 py-3 rounded-2xl rounded-bl-md flex items-center gap-1.5">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="block w-2 h-2 rounded-full bg-muted-foreground animate-dot-pulse"
          style={{ animationDelay: `${i * 0.2}s` }}
        />
      ))}
    </div>
  </div>
);

export default TypingIndicator;
