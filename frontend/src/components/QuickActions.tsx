"use client";

import { motion } from "framer-motion";

const SUGGESTIONS = [
  "¿Qué pasa si me despiden sin previo aviso?",
  "¿Cómo pido el divorcio y la pensión de mis hijos?",
  "Mi vecino no me paga una deuda, ¿qué puedo hacer?",
  "¿Cómo denuncio un fraude o un robo?",
];

export default function QuickActions({
  onSelect,
}: {
  onSelect: (text: string) => void;
}) {
  return (
    <div className="flex flex-wrap justify-center gap-2 px-4">
      {SUGGESTIONS.map((s, i) => (
        <motion.button
          key={s}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 + i * 0.05 }}
          onClick={() => onSelect(s)}
          className="rounded-full border border-turquoise/25 bg-turquoise/5 px-3.5 py-2 text-[13px] text-text-muted transition hover:border-turquoise/50 hover:bg-turquoise/10 hover:text-text-strong"
        >
          {s}
        </motion.button>
      ))}
    </div>
  );
}
