"use client";

import { Plus, History, Info, FileText, type LucideIcon } from "lucide-react";
import NicteLogo from "./NicteLogo";

export type PanelKey = "history" | "about" | "terms";

interface Props {
  activePanel: PanelKey | null;
  onNewChat: () => void;
  onOpenPanel: (key: PanelKey) => void;
}

export default function LeftNav({ activePanel, onNewChat, onOpenPanel }: Props) {
  const items: {
    key: string;
    icon: LucideIcon;
    label: string;
    onClick: () => void;
    isActive: boolean;
  }[] = [
    { key: "new", icon: Plus, label: "Nuevo", onClick: onNewChat, isActive: false },
    { key: "history", icon: History, label: "Historial", onClick: () => onOpenPanel("history"), isActive: activePanel === "history" },
    { key: "about", icon: Info, label: "Acerca", onClick: () => onOpenPanel("about"), isActive: activePanel === "about" },
    { key: "terms", icon: FileText, label: "Términos", onClick: () => onOpenPanel("terms"), isActive: activePanel === "terms" },
  ];

  return (
    <nav className="fixed left-0 top-0 z-50 flex h-full w-16 flex-col items-center gap-1 border-r border-border-soft bg-surface-deep py-4">
      <button
        onClick={onNewChat}
        title="Ir al chat de Nicté"
        aria-label="Ir al chat"
        className="mb-4 rounded-xl p-1 text-text-strong transition hover:bg-surface-muted hover:text-turquoise"
      >
        <NicteLogo withWordmark={false} className="w-9" />
      </button>

      {items.map(({ key, icon: Icon, label, onClick, isActive }) => (
        <button
          key={key}
          onClick={onClick}
          className={`flex w-14 flex-col items-center gap-1 rounded-xl py-2.5 transition ${
            isActive
              ? "bg-turquoise/15 text-turquoise"
              : "text-text-muted hover:bg-surface-muted hover:text-text-strong"
          }`}
        >
          <Icon size={20} />
          <span className="text-[9px] font-medium leading-none">{label}</span>
        </button>
      ))}
    </nav>
  );
}
