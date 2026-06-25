"use client";

import { motion } from "framer-motion";
import { AlertTriangle, ShieldAlert } from "lucide-react";
import BotAvatar from "./BotAvatar";
import CitationCard from "./CitationCard";
import type { ChatResponse } from "@/lib/api";

export type ChatMessage = {
  id: string;
  role: "user" | "bot";
  text: string;
  citations?: ChatResponse["citations"];
  legalArea?: string;
  safetyFlag?: ChatResponse["safety_flag"];
};

const AREA_LABELS: Record<string, string> = {
  laboral: "Derecho laboral",
  civil: "Derecho civil",
  penal: "Derecho penal",
  familiar: "Derecho familiar",
  mercantil: "Derecho mercantil",
  fiscal: "Derecho fiscal",
  constitucional: "Derecho constitucional",
  derechos_humanos: "Derechos humanos",
  desconocido: "Fuera de alcance",
  emergencia: "Emergencia",
};

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className={`flex items-end gap-2.5 ${isUser ? "flex-row-reverse" : ""}`}
    >
      {!isUser && <BotAvatar size={36} status={message.safetyFlag === "emergency" ? "alert" : "idle"} />}

      <div className={`flex max-w-[78%] flex-col gap-2 ${isUser ? "items-end" : "items-start"}`}>
        {!isUser && message.legalArea && (
          <span className="rounded-full bg-purple/20 px-2.5 py-0.5 text-[11px] font-medium text-purple-200/90 tracking-wide">
            {AREA_LABELS[message.legalArea] ?? message.legalArea}
          </span>
        )}

        <div
          className={`whitespace-pre-wrap rounded-2xl px-4 py-3 text-[14.5px] leading-relaxed shadow-sm ${
            isUser
              ? "rounded-br-sm bg-turquoise text-navy-deep font-medium"
              : message.safetyFlag === "emergency"
              ? "rounded-bl-sm border border-red-400/40 bg-red-950/40 text-red-100"
              : "rounded-bl-sm border border-white/5 bg-indigo/40 text-silver"
          }`}
        >
          {message.safetyFlag === "emergency" && (
            <div className="mb-2 flex items-center gap-1.5 text-red-300">
              <ShieldAlert size={15} />
              <span className="text-[12px] font-semibold uppercase tracking-wide">
                Atención inmediata
              </span>
            </div>
          )}
          {message.text}
        </div>

        {message.safetyFlag === "low_confidence" && !isUser && (
          <div className="flex items-center gap-1.5 text-[12px] text-amber-300/80">
            <AlertTriangle size={13} />
            Respuesta de baja confianza — verifica con un profesional.
          </div>
        )}

        {message.citations && message.citations.length > 0 && (
          <div className="flex w-full flex-col gap-1.5 pt-0.5">
            {message.citations.map((c) => (
              <CitationCard key={`${c.law_name}-${c.article_number}`} citation={c} />
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}
