"use client";

import { useState, useEffect, useCallback } from "react";
import { ShieldCheck, Scale, Sparkles } from "lucide-react";
import ChatWindow from "@/components/ChatWindow";
import ChatHistoryList, { type SavedConversation } from "@/components/ChatHistoryList";
import LeftNav, { type PanelKey } from "@/components/LeftNav";
import SidePanel from "@/components/SidePanel";
import AboutNicte from "@/components/AboutNicte";
import TermsConditions from "@/components/TermsConditions";
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
  const [panel, setPanel] = useState<PanelKey | null>(null);

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
    setPanel(null);
  }

  function handleLoad(conv: SavedConversation) {
    setMessages(conv.messages);
    setSessionId(conv.sessionId);
    setActiveId(conv.id);
    setInput("");
    setError(null);
    setPanel(null);
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
    <main className="relative flex min-h-screen flex-col items-center bg-background pl-16 pr-3 py-8 sm:pr-4 sm:py-12 lg:py-16">
      <HeroBackground />

      <LeftNav activePanel={panel} onNewChat={handleNewChat} onOpenPanel={setPanel} />

      <SidePanel
        open={panel === "history"}
        title="Historial de conversaciones"
        onClose={() => setPanel(null)}
      >
        <ChatHistoryList
          conversations={conversations}
          activeId={activeId}
          onNewChat={handleNewChat}
          onLoad={handleLoad}
          onDelete={handleDelete}
        />
      </SidePanel>

      <SidePanel open={panel === "about"} title="Acerca de Nicté" onClose={() => setPanel(null)}>
        <AboutNicte />
      </SidePanel>

      <SidePanel
        open={panel === "terms"}
        title="Términos y condiciones"
        onClose={() => setPanel(null)}
      >
        <TermsConditions />
      </SidePanel>

      <div className="absolute right-3 top-3 z-20 sm:right-4 sm:top-4">
        <ThemeToggle />
      </div>

      <div className="relative z-10 flex flex-col items-center text-center">
        <div className="mb-3 animate-float-slow text-text-strong sm:mb-4">
          <NicteLogo className="w-28 sm:w-36 lg:w-40" withWordmark />
        </div>
        <p className="mt-1 text-[14px] font-medium text-turquoise sm:text-[15px]">Tu aliado para hacer lo correcto.</p>
        <p className="mx-auto mt-3 max-w-md px-2 text-[14px] leading-relaxed text-text-muted sm:mt-4 sm:text-[15px]">
          Orientación legal impulsada por inteligencia artificial, diseñada para México. Habla con Nicté Bot y
          entiende tus derechos en segundos.
        </p>
        <div className="mt-6 grid w-full max-w-md grid-cols-1 gap-3 sm:mt-8 sm:max-w-none sm:grid-cols-3">
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

      <div className="relative z-10 mt-8 w-full max-w-2xl sm:mt-12">
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

      <footer className="relative z-10 mt-8 px-4 text-center text-[11px] text-text-faint sm:mt-10 sm:text-[12px]">
        Nicté no es un despacho jurídico. Nicté Bot no es un abogado — la información es orientativa y educativa.
      </footer>
    </main>
  );
}
