import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Nicté — Asistente legal IA para México",
  description:
    "Plataforma de orientación legal impulsada por inteligencia artificial, diseñada para México. Tu aliado para hacer lo correcto.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        <script
          // Apply the saved theme before first paint to avoid a flash of the
          // wrong theme. Defaults to dark when nothing is stored.
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem('nicte_theme')||'dark';if(t==='dark')document.documentElement.classList.add('dark');}catch(e){document.documentElement.classList.add('dark');}})();`,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
