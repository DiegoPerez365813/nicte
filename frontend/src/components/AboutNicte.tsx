"use client";

import { Target, Eye, Heart, RotateCcw } from "lucide-react";
import NicteLogo from "./NicteLogo";
import { logout } from "@/lib/api";

const VALUES = [
  {
    title: "Acceso a la justicia",
    text: "Creemos que entender tus derechos no debería ser un privilegio. Nicté acerca la orientación legal a cualquier persona, en cualquier lugar de México.",
  },
  {
    title: "Claridad",
    text: "Traducimos el lenguaje jurídico a explicaciones simples y accionables, sin tecnicismos innecesarios y sin dejar dudas.",
  },
  {
    title: "Honestidad",
    text: "Nicté nunca inventa leyes ni finge ser abogado. Cuando algo requiere un profesional, te lo decimos con transparencia.",
  },
  {
    title: "Respeto y empatía",
    text: "Tratamos cada situación —por difícil que sea— con calidez y sin juicios. Estás acompañado en todo momento.",
  },
  {
    title: "Empoderamiento",
    text: "No solo respondemos: te damos las herramientas, instituciones y pasos concretos para que actúes con seguridad.",
  },
];

export default function AboutNicte() {
  return (
    <div className="px-5 py-6">
      <div className="mb-6 flex flex-col items-center text-center text-text-strong">
        <NicteLogo withWordmark className="w-28" />
        <p className="mt-2 text-[13px] font-medium text-turquoise">
          Tu aliado para hacer lo correcto.
        </p>
      </div>

      <p className="mb-8 text-[13.5px] leading-relaxed text-text-muted">
        Nicté es una plataforma de orientación legal impulsada por inteligencia
        artificial, diseñada para México. Su nombre proviene del maya{" "}
        <span className="font-medium text-text-strong">nikte&apos;</span>, la flor,
        símbolo de algo que florece y se abre — como el acceso a la justicia que
        buscamos hacer posible para todas las personas.
      </p>

      <section className="mb-6">
        <div className="mb-2 flex items-center gap-2 text-turquoise">
          <Target size={17} />
          <h3 className="text-[14px] font-semibold text-text-strong">Misión</h3>
        </div>
        <p className="text-[13.5px] leading-relaxed text-text-muted">
          Democratizar el acceso a la orientación legal en México, ayudando a
          cualquier persona a entender sus derechos y las vías para ejercerlos,
          de forma clara, gratuita y sin barreras.
        </p>
      </section>

      <section className="mb-6">
        <div className="mb-2 flex items-center gap-2 text-turquoise">
          <Eye size={17} />
          <h3 className="text-[14px] font-semibold text-text-strong">Visión</h3>
        </div>
        <p className="text-[13.5px] leading-relaxed text-text-muted">
          Ser el primer punto de apoyo legal de confianza para las personas en
          México: un acompañante que oriente, eduque y conecte a cada usuario con
          las instituciones y profesionales que necesita, cerrando la brecha entre
          la ley y quienes deben beneficiarse de ella.
        </p>
      </section>

      <section>
        <div className="mb-3 flex items-center gap-2 text-turquoise">
          <Heart size={17} />
          <h3 className="text-[14px] font-semibold text-text-strong">Valores</h3>
        </div>
        <div className="space-y-3">
          {VALUES.map((v) => (
            <div
              key={v.title}
              className="rounded-xl border border-border-soft bg-surface-muted px-4 py-3"
            >
              <p className="mb-1 text-[13px] font-semibold text-text-strong">{v.title}</p>
              <p className="text-[12.5px] leading-relaxed text-text-muted">{v.text}</p>
            </div>
          ))}
        </div>
      </section>

      <div className="mt-8 border-t border-border-soft pt-6 pb-2 text-center">
        <button
          onClick={() => {
            logout(); // invalida también la cookie de sesión de Google, si existe
            sessionStorage.removeItem("nicte_onboarding_completed");
            localStorage.removeItem("nicte_username");
            localStorage.removeItem("nicte_email");
            localStorage.removeItem("nicte_registered");
            window.location.reload();
          }}
          className="inline-flex items-center gap-2 rounded-xl border border-red-500/30 bg-red-500/5 px-4 py-2 text-[12px] font-medium text-red-600 transition hover:bg-red-500/10 dark:border-red-400/20 dark:text-red-400"
        >
          <RotateCcw size={14} />
          Reiniciar Onboarding
        </button>
      </div>
    </div>
  );
}
