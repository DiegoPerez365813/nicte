"use client";

import { useEffect, useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Send } from "lucide-react";
import BotAvatar from "./BotAvatar";
import MessageBubble, { type ChatMessage } from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import DisclaimerBanner from "./DisclaimerBanner";
import QuickActions from "./QuickActions";
import { sendMessage } from "@/lib/api";

interface Props {
  messages: ChatMessage[];
  sessionId: string | null;
  input: string;
  isLoading: boolean;
  error: string | null;
  onInputChange: (v: string) => void;
  onSend: (text: string) => void;
}

export default function ChatWindow({
  messages,
  sessionId,
  input,
  isLoading,
  error,
  onInputChange,
  onSend,
}: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex h-[680px] w-full flex-col overflow-hidden rounded-3xl border border-white/10 bg-navy/80 shadow-2xl shadow-black/40 backdrop-blur-xl">
      <header className="flex items-center gap-3 border-b border-white/5 bg-navy-deep/60 px-5 py-3.5">
        <BotAvatar size={38} />
        <div>
          <p className="text-[14px] font-semibold text-white">Nicté Bot</p>
          <p className="flex items-center gap-1.5 text-[12px] text-silver/60">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
            En línea · Orientación legal mexicana
          </p>
        </div>
      </header>

      <DisclaimerBanner />

      <div ref={scrollRef} className="flex-1 space-y-5 overflow-y-auto px-5 py-5">
        <AnimatePresence initial={false}>
          {messages.map((m) => (
            <MessageBubble key={m.id} message={m} />
          ))}
        </AnimatePresence>

        {isLoading && <TypingIndicator />}

        {error && (
          <div className="rounded-xl border border-red-400/30 bg-red-950/30 px-4 py-2.5 text-[13px] text-red-200">
            {error}
          </div>
        )}

        {messages.length === 1 && (
          <div className="pt-2">
            <QuickActions onSelect={onSend} />
          </div>
        )}
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          onSend(input);
        }}
        className="flex items-center gap-2 border-t border-white/5 bg-navy-deep/60 p-3"
      >
        <input
          value={input}
          onChange={(e) => onInputChange(e.target.value)}
          placeholder="Escribe tu duda legal..."
          className="flex-1 rounded-full bg-white/5 px-4 py-2.5 text-[14px] text-white placeholder:text-silver/40 outline-none ring-1 ring-white/10 transition focus:ring-turquoise/50"
        />
        <motion.button
          whileTap={{ scale: 0.92 }}
          type="submit"
          disabled={isLoading || !input.trim()}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-turquoise text-navy-deep transition disabled:opacity-40"
        >
          <Send size={17} />
        </motion.button>
      </form>
    </div>
  );
}
