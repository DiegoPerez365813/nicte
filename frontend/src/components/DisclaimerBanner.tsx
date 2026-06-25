import { Info } from "lucide-react";

export default function DisclaimerBanner() {
  return (
    <div className="flex items-start gap-2.5 border-b border-white/5 bg-navy-deep/80 px-4 py-2.5 text-[12px] text-silver/70">
      <Info size={14} className="mt-0.5 shrink-0 text-turquoise/70" />
      <p>
        Nicté ofrece orientación informativa, no asesoría legal. Para tu caso
        específico, consulta a un abogado certificado.
      </p>
    </div>
  );
}
