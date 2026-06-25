"use client";

import Image from "next/image";
import { motion } from "framer-motion";

type Props = {
  size?: number;
  status?: "idle" | "thinking" | "alert";
};

export default function BotAvatar({ size = 44, status = "idle" }: Props) {
  const ringColor =
    status === "alert"
      ? "shadow-[0_0_0_3px_rgba(239,68,68,0.45)]"
      : status === "thinking"
      ? "shadow-[0_0_0_3px_rgba(0,188,212,0.45)]"
      : "shadow-[0_0_0_2px_rgba(0,188,212,0.25)]";

  return (
    <motion.div
      animate={status === "thinking" ? { scale: [1, 1.05, 1] } : {}}
      transition={{ repeat: Infinity, duration: 1.4 }}
      className={`relative shrink-0 rounded-full overflow-hidden bg-navy-deep ${ringColor}`}
      style={{ width: size, height: size }}
    >
      <Image
        src="/nicte-bot.png"
        alt="Nicté Bot"
        fill
        sizes={`${size}px`}
        className="object-cover"
      />
    </motion.div>
  );
}
