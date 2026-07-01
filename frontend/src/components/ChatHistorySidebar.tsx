"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, Plus, Trash2, ChevronLeft, ChevronRight, Clock } from "lucide-react";
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

export default function ChatHistorySidebar({ conversations, activeId, onNewChat, onLoad, onDelete }: Props) {
  const [collapsed, setCollapsed] = useState(false);
  const [hovered, setHovered] = useState<string | null>(null);

  return (
    <div
      className={`relative flex flex-col transition-all duration-300 ${
        collapsed ? "w-10" : "w-72"
      } shrink-0`}
    >
      {/* Toggle button */}
      <button
        onClick={() => setCollapsed((c) => !c)}
        className="absolute -left-3 top-4 z-20 flex h-6 w-6 items-center justify-center rounded-full border border-white/10 bg-navy-deep text-silver/60 shadow-md hover:text-turquoise transition"
        title={collapsed ? "Expandir historial" : "Colapsar historial"}
      >
        {collapsed ? <ChevronLeft size={13} /> : <ChevronRight size={13} />}
      </button>

      <AnimatePresence>
        {!collapsed && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.2 }}
            className="flex h-full flex-col rounded-2xl border border-white/10 bg-navy/80 backdrop-blur-xl shadow-xl overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/5 bg-navy-deep/60 px-4 py-3">
              <span className="text-[13px] font-semibold text-white">Conversaciones</span>
              <button
                onClick={onNewChat}
                className="flex items-center gap-1.5 rounded-lg bg-turquoise/10 px-2.5 py-1.5 text-[12px] font-medium text-turquoise hover:bg-turquoise/20 transition"
                title="Nueva conversación"
              >
                <Plus size={13} />
                Nueva
              </button>
            </div>

            {/* List */}
            <div className="flex-1 overflow-y-auto p-2 space-y-1">
              {conversations.length === 0 ? (
                <div className="flex flex-col items-center gap-2 py-10 text-center">
                  <MessageSquare size={28} className="text-silver/20" />
                  <p className="text-[12px] text-silver/40 leading-snug px-4">
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
                        ? "bg-turquoise/10 border border-turquoise/20"
                        : "hover:bg-white/5 border border-transparent"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <p className="line-clamp-2 text-[12.5px] font-medium text-white/90 leading-snug flex-1">
                        {conv.title}
                      </p>
                      {hovered === conv.id && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDelete(conv.id);
                          }}
                          className="shrink-0 rounded-md p-0.5 text-silver/40 hover:text-red-400 transition"
                          title="Eliminar"
                        >
                          <Trash2 size={13} />
                        </button>
                      )}
                    </div>
                    <div className="flex items-center gap-1 text-[11px] text-silver/40">
                      <Clock size={10} />
                      {relativeTime(conv.savedAt)}
                    </div>
                  </div>
                ))
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
