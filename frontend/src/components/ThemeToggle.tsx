"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Sun, Moon } from "lucide-react";

type Theme = "light" | "dark";

function applyTheme(theme: Theme) {
  const root = document.documentElement;
  root.classList.toggle("dark", theme === "dark");
  localStorage.setItem("nicte_theme", theme);
}

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>("dark");

  useEffect(() => {
    const stored = (localStorage.getItem("nicte_theme") as Theme | null) ?? "dark";
    setTheme(stored);
    applyTheme(stored);
  }, []);

  function toggle() {
    const next: Theme = theme === "dark" ? "light" : "dark";
    setTheme(next);
    applyTheme(next);
  }

  return (
    <motion.button
      whileTap={{ scale: 0.9 }}
      onClick={toggle}
      aria-label={theme === "dark" ? "Cambiar a tema claro" : "Cambiar a tema oscuro"}
      className="flex h-10 w-10 items-center justify-center rounded-full border border-border-soft bg-surface text-text-strong shadow-sm backdrop-blur transition hover:text-turquoise"
    >
      {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
    </motion.button>
  );
}
