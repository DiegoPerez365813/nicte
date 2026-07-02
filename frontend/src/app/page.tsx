"use client";

import { useState, useEffect, useCallback } from "react";
import ChatWindow from "@/components/ChatWindow";
import { type SavedConversation } from "@/components/ChatHistoryList";
import LeftNav, { type PanelKey } from "@/components/LeftNav";
import SidePanel from "@/components/SidePanel";
import HeroBackground from "@/components/HeroBackground";
import ThemeToggle from "@/components/ThemeToggle";
import { getCurrentUser, sendMessage } from "@/lib/api";
import type { ChatMessage } from "@/components/MessageBubble";
import OnboardingFlow from "@/components/OnboardingFlow";

const STORAGE_KEY = "nicte_conversations";

function getWelcomeMessage(name?: string): ChatMessage {
  const greeting = name ? `Hola ${name}, soy Nicté Bot 🌸` : "Hola, soy Nicté Bot 🌸";
  return {
    id: "welcome",
    role: "bot",
    text: `${greeting} Puedo ayudarte a entender tus derechos bajo la ley mexicana, en cualquier área: laboral, civil, penal, familiar, mercantil, fiscal y más. ¿En qué te puedo orientar?`,
  };
}

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

  const [onboardingCompleted, setOnboardingCompleted] = useState<boolean | null>(null);
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [alreadyRegistered, setAlreadyRegistered] = useState(false);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setConversations(loadConversations());

    // El flag vive en sessionStorage: persiste durante la sesión (recargas,
    // navegación) pero se borra al cerrar la pestaña/app, así el onboarding
    // vuelve a mostrarse en cada nueva apertura.
    const completed = sessionStorage.getItem("nicte_onboarding_completed") === "true";
    setOnboardingCompleted(completed);

    const storedUsername = localStorage.getItem("nicte_username") ?? "";
    setUsername(storedUsername);

    const storedEmail = localStorage.getItem("nicte_email") ?? "";
    setEmail(storedEmail);

    setAlreadyRegistered(localStorage.getItem("nicte_registered") === "true");

    setMessages([getWelcomeMessage(storedUsername)]);

    // Si hay una sesión de Google viva en el backend, refresca nombre/correo
    // desde ahí (fuente de verdad del lado servidor). Silencioso si no hay
    // sesión o el backend no está configurado todavía — no bloquea el render.
    getCurrentUser()
      .then((user) => {
        if (!user) return;
        if (user.name) {
          localStorage.setItem("nicte_username", user.name);
          setUsername(user.name);
        }
        if (user.email) {
          localStorage.setItem("nicte_email", user.email);
          setEmail(user.email);
        }
        localStorage.setItem("nicte_registered", "true");
        setAlreadyRegistered(true);
      })
      .catch(() => {});
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
    setMessages([getWelcomeMessage(username)]);
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

  function handleGoToOnboarding() {
    // Regresa al onboarding: limpia el flag de sesión y remonta el flujo.
    sessionStorage.removeItem("nicte_onboarding_completed");
    setPanel(null);
    setOnboardingCompleted(false);
  }

  function handleDelete(id: string) {
    setConversations((prev) => {
      const next = prev.filter((c) => c.id !== id);
      saveConversations(next);
      return next;
    });
    if (activeId === id) handleNewChat();
  }

  async function handleOnboardingComplete(regName?: string, initialQuery?: string, regEmail?: string) {
    if (regName) {
      localStorage.setItem("nicte_username", regName);
      setUsername(regName);
    }
    if (regEmail) {
      localStorage.setItem("nicte_email", regEmail);
      setEmail(regEmail);
    }
    if (regName || regEmail) {
      localStorage.setItem("nicte_registered", "true");
      setAlreadyRegistered(true);
    }
    sessionStorage.setItem("nicte_onboarding_completed", "true");
    setOnboardingCompleted(true);

    const initialWelcome = getWelcomeMessage(regName);

    if (initialQuery && initialQuery.trim()) {
      const userMsg: ChatMessage = { id: crypto.randomUUID(), role: "user", text: initialQuery };
      setMessages([initialWelcome, userMsg]);
      setIsLoading(true);
      setError(null);

      try {
        const res = await sendMessage(initialQuery, null);
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
        const finalMessages = [initialWelcome, userMsg, botMsg];
        setMessages(finalMessages);

        const id = crypto.randomUUID();
        setActiveId(id);
        setConversations((convs) => {
          const updated: SavedConversation = {
            id,
            title: titleFromMessages(finalMessages),
            messages: finalMessages,
            sessionId: newSessionId,
            savedAt: new Date().toISOString(),
          };
          const next = [updated, ...convs];
          saveConversations(next);
          return next;
        });
      } catch {
        setError("No pude conectar con el servidor de Nicté. Intenta de nuevo.");
      } finally {
        setIsLoading(false);
      }
    } else {
      setMessages([initialWelcome]);
    }
  }

  if (onboardingCompleted === null) {
    return null; // Evitar parpadeos de carga de localStorage
  }

  if (!onboardingCompleted) {
    return <OnboardingFlow onComplete={handleOnboardingComplete} alreadyRegistered={alreadyRegistered} />;
  }

  return (
    <main className="relative flex h-screen w-full flex-col bg-background pl-16 overflow-hidden">
      <HeroBackground />

      <LeftNav
        activePanel={panel}
        onNewChat={handleNewChat}
        onOpenPanel={setPanel}
        onLogoClick={handleGoToOnboarding}
      />

      <SidePanel
        panel={panel}
        onClose={() => setPanel(null)}
        history={{
          conversations,
          activeId,
          onNewChat: handleNewChat,
          onLoad: handleLoad,
          onDelete: handleDelete,
        }}
      />

      <div className="relative z-10 flex flex-1 flex-col w-full h-full overflow-hidden">
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
    </main>
  );
}
