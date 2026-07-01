"use client";

import { useState } from "react";
import { MessageSquare, Plus, Trash2, Clock } from "lucide-react";
import type { ChatMessage } from "./MessageBubble";

export interface SavedConversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  sessionId: string;
  savedAt: string;
}

interface Props {
  conversations: SavedConversation[];
  activeId: string | null;
  onNewChat: () => void;
  onLoad: (conv: SavedConversation) => void;
  onDelete: (id: string) => void;
}

function relativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "Ahora";
  if (mins < 60) return `Hace ${mins} min`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `Hace ${hrs} h`;
  const days = Math.floor(hrs / 24);
  if (days === 1) return "Ayer";
  if (days < 7) return `Hace ${days} días`;
  return new Date(iso).toLocaleDateString("es-MX", { day: "numeric", month: "short" });
}

export default function ChatHistoryList({ conversations, activeId, onNewChat, onLoad, onDelete }: Props) {
  const [hovered, setHovered] = useState<string | null>(null);

  return (
    <div className="flex h-full flex-col">
      <div className="p-3">
        <button
          onClick={onNewChat}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-turquoise/10 px-3 py-2.5 text-[13px] font-medium text-turquoise transition hover:bg-turquoise/20"
        >
          <Plus size={15} />
          Nueva conversación
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2 pb-3 space-y-1">
        {conversations.length === 0 ? (
          <div className="flex flex-col items-center gap-2 py-14 text-center">
            <MessageSquare size={30} className="text-text-faint" />
            <p className="px-6 text-[12.5px] leading-snug text-text-faint">
              Tus conversaciones guardadas aparecerán aquí
            </p>
          </div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              onMouseEnter={() => setHovered(conv.id)}
              onMouseLeave={() => setHovered(null)}
              onClick={() => onLoad(conv)}
              className={`group relative flex cursor-pointer flex-col gap-0.5 rounded-xl px-3 py-2.5 transition ${
                activeId === conv.id
                  ? "bg-turquoise/10 border border-turquoise/25"
                  : "hover:bg-surface-muted border border-transparent"
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <p className="line-clamp-2 flex-1 text-[13px] font-medium leading-snug text-text-strong">
                  {conv.title}
                </p>
                {hovered === conv.id && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDelete(conv.id);
                    }}
                    className="shrink-0 rounded-md p-0.5 text-text-faint transition hover:text-red-400"
                    title="Eliminar"
                  >
                    <Trash2 size={13} />
                  </button>
                )}
              </div>
              <div className="flex items-center gap-1 text-[11px] text-text-faint">
                <Clock size={10} />
                {relativeTime(conv.savedAt)}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
