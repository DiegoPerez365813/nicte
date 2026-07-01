"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ShieldCheck, Scale, Sparkles, ArrowRight } from "lucide-react";
import NicteLogo from "./NicteLogo";

const VALUE_PROPS = [
  { icon: ShieldCheck, title: "Confianza", text: "Cada respuesta se fundamenta en la ley mexicana vigente." },
  { icon: Scale, title: "Claridad", text: "Lenguaje simple, sin tecnicismos innecesarios." },
  { icon: Sparkles, title: "Empoderamiento", text: "Entiende tus derechos y actúa con seguridad." },
];

const LOADING_MS = 1900;

const item = {
  hidden: { opacity: 0, y: 18 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } },
} as const;

export default function LandingIntro({ onEnter }: { onEnter: () => void }) {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setLoaded(true), LOADING_MS);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="relative z-10 flex min-h-screen w-full flex-col items-center justify-center px-4 text-center">
      {/* Logo — always centered, appears first */}
      <motion.div
        initial={{ opacity: 0, scale: 0.92 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="text-text-strong"
      >
        <NicteLogo withWordmark className="w-36 sm:w-44" />
      </motion.div>

      {/* Loading bar — visible only during the initial load */}
      {!loaded && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="mt-10 h-1 w-52 overflow-hidden rounded-full bg-surface-muted sm:w-64"
        >
          <motion.div
            className="h-full rounded-full bg-turquoise"
            initial={{ width: "0%" }}
            animate={{ width: "100%" }}
            transition={{ duration: LOADING_MS / 1000, ease: "easeInOut" }}
          />
        </motion.div>
      )}

      {/* Hero content — unfolds progressively once loaded */}
      {loaded && (
        <motion.div
          initial="hidden"
          animate="show"
          variants={{ show: { transition: { staggerChildren: 0.2 } } }}
          className="mt-6 flex flex-col items-center"
        >
          <motion.p variants={item} className="text-[15px] font-medium text-turquoise sm:text-[16px]">
            Tu aliado para hacer lo correcto.
          </motion.p>

          <motion.p
            variants={item}
            className="mx-auto mt-4 max-w-xl text-[14px] leading-relaxed text-text-muted sm:text-[15px]"
          >
            Orientación legal impulsada por inteligencia artificial, diseñada para México.
            Habla con Nicté Bot y entiende tus derechos en segundos.
          </motion.p>

          <motion.div
            variants={item}
            className="mt-8 grid w-full max-w-3xl grid-cols-1 gap-3 sm:grid-cols-3"
          >
            {VALUE_PROPS.map(({ icon: Icon, title, text }) => (
              <div
                key={title}
                className="flex flex-col items-center gap-2 rounded-2xl border border-border-soft bg-surface-muted px-5 py-5"
              >
                <Icon size={18} className="text-turquoise" />
                <p className="text-[13px] font-medium text-text-strong">{title}</p>
                <p className="text-[12px] leading-snug text-text-muted">{text}</p>
              </div>
            ))}
          </motion.div>

          <motion.button
            variants={item}
            onClick={onEnter}
            className="mt-10 flex items-center gap-2 rounded-full bg-turquoise px-6 py-3 text-[15px] font-semibold text-navy-deep shadow-lg shadow-turquoise/20 transition hover:brightness-110"
          >
            Entrar al chat
            <ArrowRight size={18} />
          </motion.button>
        </motion.div>
      )}
    </div>
  );
}
