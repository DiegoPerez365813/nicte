"use client";

/**
 * Nicté brand logo — line-art balance scale with a lotus at its base.
 * Drawn with `currentColor` so it inverts automatically between light and
 * dark themes (set the color via a `text-*` class on the wrapper).
 */
export default function NicteLogo({
  size = 120,
  withWordmark = true,
  className = "",
}: {
  size?: number;
  withWordmark?: boolean;
  className?: string;
}) {
  const height = withWordmark ? size * 1.12 : size * 0.9;
  return (
    <svg
      width={size}
      height={height}
      viewBox="0 0 240 268"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      role="img"
      aria-label="Nicté"
    >
      {/* Top cap — three stacked horizontal lines */}
      <line x1="92" y1="40" x2="148" y2="40" />
      <line x1="86" y1="50" x2="154" y2="50" />
      <line x1="92" y1="60" x2="148" y2="60" />

      {/* Central column — three vertical lines */}
      <line x1="116" y1="66" x2="116" y2="150" />
      <line x1="120" y1="66" x2="120" y2="150" />
      <line x1="124" y1="66" x2="124" y2="150" />

      {/* Beam with pivots */}
      <line x1="66" y1="78" x2="174" y2="78" />
      <circle cx="66" cy="78" r="3.4" />
      <circle cx="174" cy="78" r="3.4" />

      {/* Left pan */}
      <line x1="66" y1="78" x2="44" y2="128" />
      <line x1="66" y1="78" x2="88" y2="128" />
      <path d="M40 128 a26 16 0 0 0 52 0" />

      {/* Right pan */}
      <line x1="174" y1="78" x2="152" y2="128" />
      <line x1="174" y1="78" x2="196" y2="128" />
      <path d="M148 128 a26 16 0 0 0 52 0" />

      {/* Lotus at the base */}
      <path d="M120 150 C104 132 96 150 108 168 C96 160 84 168 92 184 L120 184 Z" />
      <path d="M120 150 C136 132 144 150 132 168 C144 160 156 168 148 184 L120 184 Z" />
      <path d="M120 158 C112 150 112 172 120 184 C128 172 128 150 120 158 Z" />

      {/* Base feet */}
      <path d="M92 184 C86 196 84 204 84 212" />
      <path d="M148 184 C154 196 156 204 156 212" />
      <line x1="76" y1="212" x2="92" y2="212" />
      <line x1="148" y1="212" x2="164" y2="212" />
      <line x1="116" y1="184" x2="116" y2="206" />
      <line x1="124" y1="184" x2="124" y2="206" />

      {withWordmark && (
        <g
          fill="currentColor"
          stroke="none"
          style={{ letterSpacing: "0.35em" }}
        >
          <text
            x="120"
            y="252"
            textAnchor="middle"
            fontSize="30"
            fontFamily="var(--font-geist-sans), sans-serif"
            fontWeight="300"
          >
            NICTE
          </text>
        </g>
      )}
    </svg>
  );
}
