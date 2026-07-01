"use client";

import { useEffect, useState } from "react";
import { X } from "lucide-react";
import ChatHistoryList, { type SavedConversation } from "./ChatHistoryList";
import AboutNicte from "./AboutNicte";
import TermsConditions from "./TermsConditions";
import type { PanelKey } from "./LeftNav";

const TITLES: Record<PanelKey, string> = {
  history: "Historial de conversaciones",
  about: "Acerca de Nicté",
  terms: "Términos y condiciones",
};

interface HistoryProps {
  conversations: SavedConversation[];
  activeId: string | null;
  onNewChat: () => void;
  onLoad: (conv: SavedConversation) => void;
  onDelete: (id: string) => void;
}

interface Props {
  panel: PanelKey | null;
  onClose: () => void;
  history: HistoryProps;
}

export default function SidePanel({ panel, onClose, history }: Props) {
  const open = panel !== null;
  // Remember the last opened panel so its content stays visible during the
  // slide-out animation instead of blanking the moment panel becomes null.
  const [display, setDisplay] = useState<PanelKey>("history");
  useEffect(() => {
    if (panel) setDisplay(panel);
  }, [panel]);

  return (
    <>
      <div
        onClick={onClose}
        aria-hidden={!open}
        className={`fixed inset-0 z-30 bg-black/40 backdrop-blur-sm transition-opacity duration-300 ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
      />
      <aside
        className={`fixed left-16 top-0 z-40 flex h-full w-[calc(100%-4rem)] max-w-sm flex-col border-r border-border-soft bg-surface-deep shadow-2xl transition-transform duration-300 ease-out ${
          open ? "translate-x-0" : "-translate-x-[calc(100%+4rem)]"
        }`}
      >
        <header className="flex items-center justify-between border-b border-border-soft px-5 py-4">
          <h2 className="text-[15px] font-semibold text-text-strong">{TITLES[display]}</h2>
          <button
            onClick={onClose}
            aria-label="Cerrar"
            className="rounded-lg p-1 text-text-muted transition hover:bg-surface-muted hover:text-text-strong"
          >
            <X size={18} />
          </button>
        </header>
        <div className="flex-1 overflow-y-auto">
          {display === "history" && <ChatHistoryList {...history} />}
          {display === "about" && <AboutNicte />}
          {display === "terms" && <TermsConditions />}
        </div>
      </aside>
    </>
  );
}
