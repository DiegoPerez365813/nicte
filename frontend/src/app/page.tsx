import Image from "next/image";
import { ShieldCheck, Scale, Sparkles } from "lucide-react";
import ChatWindow from "@/components/ChatWindow";
import HeroBackground from "@/components/HeroBackground";

const VALUE_PROPS = [
  {
    icon: ShieldCheck,
    title: "Confianza",
    text: "Cada respuesta se fundamenta en la ley mexicana vigente.",
  },
  {
    icon: Scale,
    title: "Claridad",
    text: "Lenguaje simple, sin tecnicismos innecesarios.",
  },
  {
    icon: Sparkles,
    title: "Empoderamiento",
    text: "Entiende tus derechos y actúa con seguridad.",
  },
];

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center bg-navy-deep px-4 py-16">
      <HeroBackground />

      <div className="relative z-10 flex flex-col items-center text-center">
        <div className="mb-6 h-20 w-32 animate-float-slow">
          <Image
            src="/nicte-logo.png"
            alt="Nicté"
            width={128}
            height={80}
            className="h-full w-full object-contain"
            priority
          />
        </div>

        <h1 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl">
          Nicté
        </h1>
        <p className="mt-2 text-[15px] font-medium text-turquoise/90">
          Tu aliado para hacer lo correcto.
        </p>
        <p className="mx-auto mt-4 max-w-md text-[15px] leading-relaxed text-silver/70">
          Orientación legal impulsada por inteligencia artificial, diseñada
          para México. Habla con Nicté Bot y entiende tus derechos en
          segundos.
        </p>

        <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-3">
          {VALUE_PROPS.map(({ icon: Icon, title, text }) => (
            <div
              key={title}
              className="flex flex-col items-center gap-2 rounded-2xl border border-white/5 bg-white/[0.02] px-4 py-4 sm:w-40"
            >
              <Icon size={18} className="text-turquoise" />
              <p className="text-[13px] font-medium text-white">{title}</p>
              <p className="text-[12px] leading-snug text-silver/60">{text}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="relative z-10 mt-12 w-full">
        <ChatWindow />
      </div>

      <footer className="relative z-10 mt-10 text-center text-[12px] text-silver/40">
        Nicté no es un despacho jurídico. Nicté Bot no es un abogado — la
        información es orientativa y educativa.
      </footer>
    </main>
  );
}
