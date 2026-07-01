import { Info } from "lucide-react";

export default function DisclaimerBanner() {
  return (
    <div className="flex items-start gap-2.5 border-b border-border-soft bg-surface-deep px-4 py-2.5 text-[12px] text-text-muted">
      <Info size={14} className="mt-0.5 shrink-0 text-turquoise" />
      <p>
        Nicté ofrece orientación informativa, no asesoría legal. Para tu caso
        específico, consulta a un abogado certificado.
      </p>
    </div>
  );
}
