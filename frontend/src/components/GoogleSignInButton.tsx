"use client";

import { useEffect, useRef, useState } from "react";
import { signInWithGoogle, type NicteUser } from "@/lib/api";

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: {
            client_id: string;
            callback: (response: { credential: string }) => void;
          }) => void;
          renderButton: (parent: HTMLElement, options: Record<string, unknown>) => void;
        };
      };
    };
  }
}

const CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

export default function GoogleSignInButton({
  onSuccess,
  onError,
}: {
  onSuccess: (user: NicteUser) => void;
  onError?: (message: string) => void;
}) {
  const buttonRef = useRef<HTMLDivElement>(null);
  // Lazy initializer covers the "script already loaded by an earlier mount"
  // case without needing a setState call inside the effect body below.
  const [scriptLoaded, setScriptLoaded] = useState(
    () => typeof window !== "undefined" && !!window.google
  );

  useEffect(() => {
    if (!CLIENT_ID || scriptLoaded) return;

    const existing = document.querySelector<HTMLScriptElement>(
      'script[src="https://accounts.google.com/gsi/client"]'
    );
    if (existing) {
      existing.addEventListener("load", () => setScriptLoaded(true), { once: true });
      return;
    }

    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = () => setScriptLoaded(true);
    document.head.appendChild(script);
    // Keep the script cached across mounts — Google's client is safe to
    // share, no need to remove it on unmount.
  }, [scriptLoaded]);

  useEffect(() => {
    if (!scriptLoaded || !CLIENT_ID || !buttonRef.current || !window.google) return;

    window.google.accounts.id.initialize({
      client_id: CLIENT_ID,
      callback: async (response) => {
        try {
          const user = await signInWithGoogle(response.credential);
          onSuccess(user);
        } catch (err) {
          onError?.(err instanceof Error ? err.message : "No se pudo iniciar sesión con Google.");
        }
      },
    });

    window.google.accounts.id.renderButton(buttonRef.current, {
      theme: "outline",
      size: "large",
      width: 320,
      text: "continue_with",
      locale: "es",
    });
  }, [scriptLoaded, onSuccess, onError]);

  if (!CLIENT_ID) {
    // No Client ID configured yet — hide the button instead of rendering a
    // broken widget. See render.yaml / Vercel env for NEXT_PUBLIC_GOOGLE_CLIENT_ID.
    return null;
  }

  return <div ref={buttonRef} className="flex justify-center" />;
}
