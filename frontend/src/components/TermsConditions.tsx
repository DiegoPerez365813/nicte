"use client";

const SECTIONS = [
  {
    title: "1. Naturaleza del servicio",
    body: "Nicté es una herramienta informativa y educativa impulsada por inteligencia artificial. Ofrece orientación general sobre el sistema jurídico mexicano, pero NO constituye asesoría legal, no crea una relación abogado-cliente y no sustituye la consulta con un profesional del derecho certificado.",
  },
  {
    title: "2. Nicté no es un abogado",
    body: "Las respuestas de Nicté Bot son generadas automáticamente y pueden contener imprecisiones u omisiones. Para cualquier decisión que afecte tus derechos, obligaciones o patrimonio, debes consultar a un abogado o a la Defensoría Pública correspondiente.",
  },
  {
    title: "3. Uso responsable",
    body: "Te comprometes a usar Nicté de buena fe y únicamente con fines lícitos. No debes utilizar la plataforma para obtener orientación destinada a cometer delitos, evadir la ley o perjudicar a terceros.",
  },
  {
    title: "4. Emergencias",
    body: "Nicté no puede intervenir en situaciones de riesgo inmediato. Si estás en peligro, comunícate de inmediato al 911, o a la línea contra la violencia (*088). Nicté no es un servicio de emergencia.",
  },
  {
    title: "5. Privacidad y datos",
    body: "El historial de tus conversaciones se guarda localmente en tu propio navegador (localStorage) y puedes eliminarlo en cualquier momento. Los mensajes que envías se procesan para generar una respuesta. Evita compartir datos sensibles como contraseñas, números de tarjeta o identificaciones oficiales.",
  },
  {
    title: "6. Limitación de responsabilidad",
    body: "Nicté y sus creadores no se hacen responsables por daños o perjuicios derivados del uso o interpretación de la información proporcionada. El usuario es el único responsable de las decisiones que tome con base en dicha información.",
  },
  {
    title: "7. Propiedad y contenido",
    body: "Las referencias a leyes, códigos y artículos provienen de fuentes oficiales de acceso público. La marca, el diseño y el funcionamiento de Nicté son propiedad de sus creadores.",
  },
  {
    title: "8. Cambios",
    body: "Estos términos pueden actualizarse en cualquier momento. El uso continuado de Nicté implica la aceptación de la versión vigente.",
  },
];

export default function TermsConditions() {
  return (
    <div className="px-5 py-6">
      <p className="mb-6 text-[12.5px] leading-relaxed text-text-muted">
        Al utilizar Nicté aceptas los siguientes términos y condiciones. Léelos
        con atención.
      </p>

      <div className="space-y-5">
        {SECTIONS.map((s) => (
          <section key={s.title}>
            <h3 className="mb-1.5 text-[13.5px] font-semibold text-text-strong">{s.title}</h3>
            <p className="text-[12.5px] leading-relaxed text-text-muted">{s.body}</p>
          </section>
        ))}
      </div>

      <p className="mt-8 border-t border-border-soft pt-4 text-[11px] leading-relaxed text-text-faint">
        Nicté no es un despacho jurídico. La información es orientativa y educativa.
        Última actualización: julio 2026.
      </p>
    </div>
  );
}
