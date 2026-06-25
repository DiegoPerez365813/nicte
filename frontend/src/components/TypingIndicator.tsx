"use client";

import { motion } from "framer-motion";
import BotAvatar from "./BotAvatar";

export default function TypingIndicator() {
  return (
    <div className="flex items-end gap-2.5">
      <BotAvatar size={36} status="thinking" />
      <div className="flex items-center gap-1.5 rounded-2xl rounded-bl-sm bg-indigo/40 px-4 py-3.5 border border-white/5">
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            className="h-2 w-2 rounded-full bg-turquoise/80"
            animate={{ opacity: [0.3, 1, 0.3], y: [0, -3, 0] }}
            transition={{ repeat: Infinity, duration: 1, delay: i * 0.15 }}
          />
        ))}
      </div>
    </div>
  );
}
