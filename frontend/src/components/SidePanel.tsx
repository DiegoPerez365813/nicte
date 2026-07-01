"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";

interface Props {
  open: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}

export default function SidePanel({ open, title, onClose, children }: Props) {
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            className="fixed inset-0 z-30 bg-black/40 backdrop-blur-sm"
            onClick={onClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />
          <motion.aside
            className="fixed left-16 top-0 z-40 flex h-full w-[calc(100%-4rem)] max-w-sm flex-col border-r border-border-soft bg-surface-deep shadow-2xl"
            initial={{ x: "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: "-100%" }}
            transition={{ type: "tween", duration: 0.25, ease: "easeOut" }}
          >
            <header className="flex items-center justify-between border-b border-border-soft px-5 py-4">
              <h2 className="text-[15px] font-semibold text-text-strong">{title}</h2>
              <button
                onClick={onClose}
                aria-label="Cerrar"
                className="rounded-lg p-1 text-text-muted transition hover:bg-surface-muted hover:text-text-strong"
              >
                <X size={18} />
              </button>
            </header>
            <div className="flex-1 overflow-y-auto">{children}</div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
