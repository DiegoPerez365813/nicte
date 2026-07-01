"use client";

import { useEffect, useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Send } from "lucide-react";
import BotAvatar from "./BotAvatar";
import MessageBubble, { type ChatMessage } from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import DisclaimerBanner from "./DisclaimerBanner";
import QuickActions from "./QuickActions";
import ThemeToggle from "./ThemeToggle";

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
    <div className="flex h-full w-full flex-col overflow-hidden bg-transparent">
      <header className="flex items-center justify-between border-b border-border-soft bg-surface-deep px-6 py-4">
        <div className="flex items-center gap-3">
          <BotAvatar size={52} />
          <div>
            <p className="text-[15px] font-semibold text-text-strong">Nicté Bot</p>
            <p className="flex items-center gap-1.5 text-[12px] text-text-muted">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              En línea · Orientación legal mexicana
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle />
        </div>
      </header>

      <DisclaimerBanner />

      <div ref={scrollRef} className="flex-1 overflow-y-auto py-5">
        <div className="mx-auto max-w-3xl px-5 space-y-5">
          <AnimatePresence initial={false}>
            {messages.map((m) => (
              <MessageBubble key={m.id} message={m} />
            ))}
          </AnimatePresence>

          {isLoading && <TypingIndicator />}

          {error && (
            <div className="rounded-xl border border-red-400/30 bg-red-50 px-4 py-2.5 text-[13px] text-red-700 dark:bg-red-950/30 dark:text-red-200">
              {error}
            </div>
          )}

          {messages.length === 1 && (
            <div className="pt-2">
              <QuickActions onSelect={onSend} />
            </div>
          )}
        </div>
      </div>

      <div className="border-t border-border-soft bg-surface-deep p-4">
        <div className="mx-auto max-w-3xl flex flex-col gap-2">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              onSend(input);
            }}
            className="flex items-center gap-2"
          >
            <input
              value={input}
              onChange={(e) => onInputChange(e.target.value)}
              placeholder="Escribe tu duda legal..."
              className="flex-1 rounded-full bg-surface-muted px-4 py-2.5 text-[14px] text-text-strong placeholder:text-text-faint outline-none ring-1 ring-border-soft transition focus:ring-turquoise/60"
            />
            <motion.button
              whileTap={{ scale: 0.92 }}
              type="submit"
              disabled={isLoading || input.trim().length === 0}
              className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-turquoise text-navy-deep transition disabled:opacity-40"
            >
              <Send size={17} />
            </motion.button>
          </form>
          <p className="text-center text-[11px] text-text-faint">
            Nicté no es un despacho jurídico. Nicté Bot no es un abogado — la orientación es informativa y educativa.
          </p>
        </div>
      </div>
    </div>
  );
}
