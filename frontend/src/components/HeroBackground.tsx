"use client";

export default function HeroBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute -top-32 left-1/4 h-96 w-96 animate-glow-pulse rounded-full bg-purple/30 blur-3xl" />
      <div className="absolute top-1/3 -right-20 h-80 w-80 animate-glow-pulse rounded-full bg-turquoise/20 blur-3xl [animation-delay:1.2s]" />
      <div className="absolute bottom-0 left-1/3 h-72 w-72 animate-glow-pulse rounded-full bg-indigo/30 blur-3xl [animation-delay:2.4s]" />

      <svg className="absolute inset-0 h-full w-full opacity-[0.07]" aria-hidden="true">
        <defs>
          <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
            <path d="M48 0 L0 0 0 48" fill="none" stroke="#00BCD4" strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
    </div>
  );
}
