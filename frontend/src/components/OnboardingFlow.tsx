"use client";

import { useEffect, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ShieldCheck, Scale, Sparkles, ArrowRight, User, Mail, ChevronRight, MessageSquare } from "lucide-react";
import NicteLogo from "./NicteLogo";
import TermsConditions from "./TermsConditions";

interface Props {
  onComplete: (username?: string, initialQuery?: string) => void;
}

type OnboardingStep = "splash" | "welcome" | "terms" | "register" | "guided";

const VALUE_PROPS = [
  { icon: ShieldCheck, title: "Confianza", text: "Cada respuesta se fundamenta en la ley mexicana vigente." },
  { icon: Scale, title: "Claridad", text: "Lenguaje simple, sin tecnicismos innecesarios." },
  { icon: Sparkles, title: "Empoderamiento", text: "Entiende tus derechos y actúa con seguridad." },
];

const SUGGESTED_QUERIES = [
  {
    title: "Vacaciones Anuales",
    query: "¿Cuántos días de vacaciones me corresponden si llevo 2 años trabajando?",
    desc: "Materia Laboral · Conoce tus días de descanso obligatorios.",
  },
  {
    title: "Despido Injustificado",
    query: "¿Qué me corresponde por ley si me despiden sin previo aviso?",
    desc: "Materia Laboral · Liquidación, finiquito e indemnizaciones.",
  },
  {
    title: "Derechos en Tránsito",
    query: "¿Es legal que un policía de tránsito me pida bajar del auto o retenga mi licencia?",
    desc: "Materia de Tránsito / Penal · Límites de la autoridad en detenciones.",
  },
  {
    title: "Pensión Alimenticia",
    query: "¿Cómo puedo solicitar la pensión alimenticia de mis hijos y cuánto porcentaje aplica?",
    desc: "Materia Familiar · Obligaciones, demandas y montos.",
  },
];

export default function OnboardingFlow({ onComplete }: Props) {
  const [step, setStep] = useState<OnboardingStep>("splash");
  const [progress, setProgress] = useState(0);
  const [hasScrolledToBottom, setHasScrolledToBottom] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Paso 1: Splash Screen timer
  useEffect(() => {
    if (step !== "splash") return;
    const duration = 2000;
    const intervalTime = 50;
    const stepAmount = 100 / (duration / intervalTime);

    const timer = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(timer);
          setStep("welcome");
          return 100;
        }
        return prev + stepAmount;
      });
    }, intervalTime);

    return () => clearInterval(timer);
  }, [step]);

  // Paso 3: Scroll obligatorio en los términos
  const handleScroll = () => {
    const el = scrollContainerRef.current;
    if (!el) return;
    
    // Si la suma del scroll superior y el alto del cliente es igual o mayor al alto total
    // (con un margen de tolerancia de 15px para evitar problemas de redondeo decimal)
    const reachedBottom = el.scrollTop + el.clientHeight >= el.scrollHeight - 15;
    if (reachedBottom) {
      setHasScrolledToBottom(true);
    }
  };

  const handleRegisterSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const cleanName = name.trim();
    if (cleanName) {
      onComplete(cleanName);
    } else {
      setStep("guided");
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background px-4 py-6 md:py-10">
      {/* Background radial glow */}
      <div className="absolute inset-0 bg-radial-[circle_at_center,var(--hero-glow)_0%,transparent_70%] opacity-80" />

      <div className="relative z-10 w-full max-w-2xl overflow-hidden rounded-3xl border border-border-soft bg-surface shadow-2xl backdrop-blur-xl">
        <AnimatePresence mode="wait">
          {/* 1. SPLASH SCREEN */}
          {step === "splash" && (
            <motion.div
              key="splash"
              initial={{ opacity: 1 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="flex min-h-[460px] flex-col items-center justify-center p-8 text-center"
            >
              <motion.div
                initial={{ scale: 0.85, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.6, ease: "easeOut" }}
                className="text-text-strong"
              >
                <NicteLogo withWordmark className="w-36 sm:w-44" />
              </motion.div>
              <div className="mt-10 h-1.5 w-52 overflow-hidden rounded-full bg-surface-muted sm:w-64">
                <div
                  className="h-full rounded-full bg-turquoise transition-all duration-75"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="mt-4 text-[12px] text-text-faint font-medium tracking-wide">
                CARGANDO CONOCIMIENTO LEGAL...
              </p>
            </motion.div>
          )}

          {/* 2. BIENVENIDA */}
          {step === "welcome" && (
            <motion.div
              key="welcome"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="flex min-h-[480px] flex-col items-center justify-between p-6 sm:p-10 text-center"
            >
              <div className="flex flex-col items-center">
                <NicteLogo withWordmark={false} className="w-16 text-text-strong" />
                <h1 className="mt-4 text-[22px] font-bold text-text-strong sm:text-[26px]">
                  Te damos la bienvenida a Nicté
                </h1>
                <p className="mt-1.5 text-[14px] font-medium text-turquoise sm:text-[15px]">
                  Tu aliado para hacer lo correcto.
                </p>
                <p className="mx-auto mt-4 max-w-lg text-[13.5px] leading-relaxed text-text-muted">
                  Nicté es una plataforma informativa diseñada para ayudarte a entender el sistema jurídico mexicano.
                  Habla de manera sencilla y clara con nuestro bot inteligente.
                </p>
              </div>

              <div className="my-6 grid w-full grid-cols-1 gap-3 sm:grid-cols-3">
                {VALUE_PROPS.map(({ icon: Icon, title, text }) => (
                  <div
                    key={title}
                    className="flex flex-col items-center gap-1.5 rounded-2xl border border-border-soft bg-surface-muted px-4 py-4 text-center"
                  >
                    <Icon size={18} className="text-turquoise" />
                    <p className="text-[13px] font-semibold text-text-strong">{title}</p>
                    <p className="text-[12px] leading-snug text-text-muted">{text}</p>
                  </div>
                ))}
              </div>

              <button
                onClick={() => setStep("terms")}
                className="flex items-center gap-2 rounded-full bg-turquoise px-6 py-2.5 text-[14px] font-semibold text-navy-deep shadow-lg shadow-turquoise/20 transition hover:brightness-110"
              >
                Comenzar
                <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {/* 3. TÉRMINOS Y CONDICIONES (SCROLL OBLIGATORIO) */}
          {step === "terms" && (
            <motion.div
              key="terms"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col p-5 sm:p-8"
            >
              <div className="mb-4">
                <h2 className="text-[18px] font-bold text-text-strong">Términos y condiciones</h2>
                <p className="text-[12.5px] text-text-muted mt-1">
                  Es indispensable que leas y comprendas el aviso legal de IA antes de ingresar.
                </p>
              </div>

              {/* Scrollable Container */}
              <div
                ref={scrollContainerRef}
                onScroll={handleScroll}
                className="h-[220px] overflow-y-auto rounded-2xl border border-border-hard bg-surface-deep/50"
              >
                <TermsConditions />
              </div>

              <div className="mt-5 flex flex-col items-center justify-between gap-4 border-t border-border-soft pt-4 sm:flex-row">
                <p className="text-[12px] text-center sm:text-left text-text-faint">
                  {!hasScrolledToBottom ? (
                    <span className="text-turquoise animate-pulse font-medium">
                      ⚠️ Desplaza el texto hasta el final para habilitar la aceptación.
                    </span>
                  ) : (
                    "✓ Has leído todo el documento."
                  )}
                </p>

                <button
                  disabled={!hasScrolledToBottom}
                  onClick={() => setStep("register")}
                  className="flex items-center gap-2 rounded-full bg-turquoise px-6 py-2.5 text-[14px] font-semibold text-navy-deep shadow-lg shadow-turquoise/20 transition hover:brightness-110 disabled:cursor-not-allowed disabled:bg-surface-muted disabled:text-text-faint disabled:shadow-none"
                >
                  Aceptar y continuar
                  <ArrowRight size={16} />
                </button>
              </div>
            </motion.div>
          )}

          {/* 4. REGISTRO OPCIONAL */}
          {step === "register" && (
            <motion.div
              key="register"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col p-6 sm:p-10"
            >
              <div className="text-center">
                <h2 className="text-[18px] font-bold text-text-strong">Registro opcional</h2>
                <p className="mt-1.5 text-[13px] text-text-muted max-w-md mx-auto">
                  Registra tu nombre para que Nicté Bot pueda saludarte y personalizar tu orientación legal. Puedes omitir este paso si lo deseas.
                </p>
              </div>

              <form onSubmit={handleRegisterSubmit} className="my-6 space-y-4">
                <div className="relative">
                  <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-text-faint">
                    <User size={16} />
                  </div>
                  <input
                    type="text"
                    placeholder="Tu nombre completo (opcional)"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full rounded-2xl bg-surface-deep px-11 py-3 text-[14px] text-text-strong placeholder:text-text-faint outline-none ring-1 ring-border-soft transition focus:ring-turquoise/60"
                  />
                </div>

                <div className="relative">
                  <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-text-faint">
                    <Mail size={16} />
                  </div>
                  <input
                    type="email"
                    placeholder="Tu correo electrónico (opcional)"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full rounded-2xl bg-surface-deep px-11 py-3 text-[14px] text-text-strong placeholder:text-text-faint outline-none ring-1 ring-border-soft transition focus:ring-turquoise/60"
                  />
                </div>

                <div className="pt-2 flex flex-col gap-3 sm:flex-row sm:justify-between sm:items-center">
                  <button
                    type="button"
                    onClick={() => setStep("guided")}
                    className="w-full sm:w-auto text-[13.5px] font-medium text-text-muted hover:text-turquoise transition py-2 text-center"
                  >
                    Continuar como invitado
                  </button>

                  <button
                    type="submit"
                    className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-full bg-turquoise px-6 py-2.5 text-[14px] font-semibold text-navy-deep shadow-lg shadow-turquoise/20 transition hover:brightness-110"
                  >
                    Registrarse
                    <ArrowRight size={16} />
                  </button>
                </div>
              </form>
            </motion.div>
          )}

          {/* 5. CONSULTA GUIADA */}
          {step === "guided" && (
            <motion.div
              key="guided"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col p-5 sm:p-8"
            >
              <div className="mb-4 text-center">
                <h2 className="text-[18px] font-bold text-text-strong">Tu primera consulta</h2>
                <p className="text-[13px] text-text-muted mt-1.5 max-w-md mx-auto">
                  Selecciona alguna de las preguntas sugeridas sobre temas frecuentes para ver cómo funciona Nicté, o ve al chat libremente.
                </p>
              </div>

              <div className="grid grid-cols-1 gap-2.5 my-4 sm:grid-cols-2">
                {SUGGESTED_QUERIES.map((q) => (
                  <button
                    key={q.title}
                    onClick={() => onComplete(name.trim() || undefined, q.query)}
                    className="group flex flex-col items-left text-left p-3.5 rounded-2xl border border-border-soft bg-surface-deep/50 hover:bg-turquoise/10 hover:border-turquoise/30 transition duration-200"
                  >
                    <div className="flex items-center justify-between w-full">
                      <p className="text-[13.5px] font-semibold text-text-strong group-hover:text-turquoise transition">
                        {q.title}
                      </p>
                      <ChevronRight size={15} className="text-text-faint group-hover:text-turquoise transition transform group-hover:translate-x-1" />
                    </div>
                    <p className="text-[11px] text-text-faint mt-0.5 tracking-wide uppercase">
                      {q.desc.split(" · ")[0]}
                    </p>
                    <p className="text-[12px] text-text-muted mt-1.5 leading-snug line-clamp-2">
                      {q.query}
                    </p>
                  </button>
                ))}
              </div>

              <div className="mt-4 flex justify-center border-t border-border-soft pt-4">
                <button
                  onClick={() => onComplete(name.trim() || undefined)}
                  className="flex items-center gap-2 rounded-full border border-border-hard px-6 py-2 text-[13.5px] font-medium text-text-strong hover:bg-surface-muted transition"
                >
                  <MessageSquare size={15} />
                  Ir al chat directamente
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
