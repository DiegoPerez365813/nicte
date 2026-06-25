"use client";

import { Scale, ShieldCheck, ExternalLink } from "lucide-react";
import type { Citation } from "@/lib/api";

export default function CitationCard({ citation }: { citation: Citation }) {
  const isDefense = citation.kind === "defensa";

  return (
    <a
      href={citation.source_url}
      target="_blank"
      rel="noopener noreferrer"
      className={`group flex items-start gap-3 rounded-xl border px-3.5 py-2.5 transition ${
        isDefense
          ? "border-emerald-400/25 bg-emerald-950/20 hover:border-emerald-400/50 hover:bg-emerald-950/30"
          : "border-turquoise/20 bg-navy-deep/60 hover:border-turquoise/50 hover:bg-navy-deep"
      }`}
    >
      <div
        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
          isDefense ? "bg-emerald-400/10 text-emerald-300" : "bg-turquoise/10 text-turquoise"
        }`}
      >
        {isDefense ? <ShieldCheck size={16} /> : <Scale size={16} />}
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <p className="truncate text-[13px] font-medium text-silver">{citation.law_name}</p>
          {isDefense && (
            <span className="shrink-0 rounded-full bg-emerald-400/15 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-emerald-300">
              Tu defensa
            </span>
          )}
        </div>
        <p className="text-[12px] text-silver/60">
          Artículo {citation.article_number} · {citation.jurisdiction}
        </p>
        {citation.plain_summary && (
          <p className="mt-1 text-[12.5px] leading-snug text-silver/80">{citation.plain_summary}</p>
        )}
      </div>
      <ExternalLink
        size={14}
        className={`mt-1 shrink-0 transition ${
          isDefense ? "text-silver/40 group-hover:text-emerald-300" : "text-silver/40 group-hover:text-turquoise"
        }`}
      />
    </a>
  );
}
