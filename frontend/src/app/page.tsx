"use client";

import { useState, useEffect, useCallback } from "react";
import { ShieldCheck, Scale, Sparkles } from "lucide-react";
import ChatWindow from "@/components/ChatWindow";
import ChatHistorySidebar, { type SavedConversation } from "@/components/ChatHistorySidebar";
import HeroBackground from "@/components/HeroBackground";
import NicteLogo from "@/components/NicteLogo";
import ThemeToggle from "@/components/ThemeToggle";
import { sendMessage } from "@/lib/api";
import type { ChatMessage } from "@/components/MessageBubble";

const STORAGE_KEY = "nicte_conversations";

const WELCOME: ChatMessage = {
  id: "welcome",
  role: "bot",
  text: "Hola, soy Nicté Bot 🌸 Puedo ayudarte a entender tus derechos bajo la ley mexicana, en cualquier área: laboral, civil, penal, familiar, mercantil, fiscal y más. ¿En qué te puedo orientar?",
};

const VALUE_PROPS = [
  { icon: ShieldCheck, title: "Confianza", text: "Cada respuesta se fundamenta en la ley mexicana vigente." },
  { icon: Scale, title: "Claridad", text: "Lenguaje simple, sin tecnicismos innecesarios." },
  { icon: Sparkles, title: "Empoderamiento", text: "Entiende tus derechos y actúa con seguridad." },
];

function titleFromMessages(messages: ChatMessage[]): string {
  const first = messages.find((m) => m.role === "user");
  if (!first) return "Nueva conversación";
  return first.text.length > 60 ? first.text.slice(0, 57) + "…" : first.text;
}

function loadConversations(): SavedConversation[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]");
  } catch {
    return [];
  }
}

function saveConversations(convs: SavedConversation[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(convs));
}

export default function Home() {
  const [conversations, setConversations] = useState<SavedConversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setConversations(loadConversations());
  }, []);

  const persistCurrent = useCallback(
    (msgs: ChatMessage[], sid: string | null, existingId: string | null) => {
      const hasUserMessage = msgs.some((m) => m.role === "user");
      if (!hasUserMessage || !sid) return existingId;

      setConversations((prev) => {
        const id = existingId ?? crypto.randomUUID();
        const updated: SavedConversation = {
          id,
          title: titleFromMessages(msgs),
          messages: msgs,
          sessionId: sid,
          savedAt: new Date().toISOString(),
        };
        const filtered = prev.filter((c) => c.id !== id);
        const next = [updated, ...filtered];
        saveConversations(next);
        return next;
      });

      return existingId ?? null;
    },
    []
  );

  async function handleSend(text: string) {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    const userMsg: ChatMessage = { id: crypto.randomUUID(), role: "user", text: trimmed };
    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setInput("");
    setIsLoading(true);
    setError(null);

    try {
      const res = await sendMessage(trimmed, sessionId);
      const newSessionId = res.session_id;
      setSessionId(newSessionId);

      const botMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: "bot",
        text: res.answer,
        citations: res.citations,
        legalArea: res.legal_area,
        safetyFlag: res.safety_flag,
      };
      const finalMessages = [...nextMessages, botMsg];
      setMessages(finalMessages);

      setActiveId((prev) => {
        const id = prev ?? crypto.randomUUID();
        setConversations((convs) => {
          const updated: SavedConversation = {
            id,
            title: titleFromMessages(finalMessages),
            messages: finalMessages,
            sessionId: newSessionId,
            savedAt: new Date().toISOString(),
          };
          const filtered = convs.filter((c) => c.id !== id);
          const next = [updated, ...filtered];
          saveConversations(next);
          return next;
        });
        return id;
      });
    } catch {
      setError("No pude conectar con el servidor de Nicté. Intenta de nuevo.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleNewChat() {
    setMessages([WELCOME]);
    setSessionId(null);
    setActiveId(null);
    setInput("");
    setError(null);
  }

  function handleLoad(conv: SavedConversation) {
    setMessages(conv.messages);
    setSessionId(conv.sessionId);
    setActiveId(conv.id);
    setInput("");
    setError(null);
  }

  function handleDelete(id: string) {
    setConversations((prev) => {
      const next = prev.filter((c) => c.id !== id);
      saveConversations(next);
      return next;
    });
    if (activeId === id) handleNewChat();
  }

  return (
    <main className="relative flex min-h-screen flex-col items-center bg-background px-4 py-16">
      <HeroBackground />

      <div className="absolute right-4 top-4 z-20">
        <ThemeToggle />
      </div>

      <div className="relative z-10 flex flex-col items-center text-center">
        <div className="mb-4 animate-float-slow text-text-strong">
          <NicteLogo size={150} withWordmark />
        </div>
        <p className="mt-1 text-[15px] font-medium text-turquoise">Tu aliado para hacer lo correcto.</p>
        <p className="mx-auto mt-4 max-w-md text-[15px] leading-relaxed text-text-muted">
          Orientación legal impulsada por inteligencia artificial, diseñada para México. Habla con Nicté Bot y
          entiende tus derechos en segundos.
        </p>
        <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-3">
          {VALUE_PROPS.map(({ icon: Icon, title, text }) => (
            <div
              key={title}
              className="flex flex-col items-center gap-2 rounded-2xl border border-border-soft bg-surface-muted px-4 py-4 sm:w-40"
            >
              <Icon size={18} className="text-turquoise" />
              <p className="text-[13px] font-medium text-text-strong">{title}</p>
              <p className="text-[12px] leading-snug text-text-muted">{text}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="relative z-10 mt-12 w-full max-w-5xl flex gap-4 items-start">
        <div className="flex-1 min-w-0">
          <ChatWindow
            messages={messages}
            sessionId={sessionId}
            input={input}
            isLoading={isLoading}
            error={error}
            onInputChange={setInput}
            onSend={handleSend}
          />
        </div>
        <ChatHistorySidebar
          conversations={conversations}
          activeId={activeId}
          onNewChat={handleNewChat}
          onLoad={handleLoad}
          onDelete={handleDelete}
        />
      </div>

      <footer className="relative z-10 mt-10 text-center text-[12px] text-text-faint">
        Nicté no es un despacho jurídico. Nicté Bot no es un abogado — la información es orientativa y educativa.
      </footer>
    </main>
  );
}
