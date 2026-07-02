export type Citation = {
  law_name: string;
  article_number: string;
  jurisdiction: string;
  source_url: string;
  relevance_score: number;
  kind: "fundamento" | "defensa";
  plain_summary?: string | null;
};

export type SafetyFlag = "emergency" | "out_of_scope" | "low_confidence" | null;

export type ChatResponse = {
  session_id: string;
  answer: string;
  citations: Citation[];
  legal_area: string;
  safety_flag: SafetyFlag;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function sendMessage(
  message: string,
  sessionId: string | null
): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/v1/chat/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!res.ok) {
    throw new Error(`Nicté backend respondió con error ${res.status}`);
  }

  return res.json();
}

export type NicteUser = {
  name: string | null;
  email: string | null;
  picture: string | null;
};

// Auth calls always use credentials:"include" so the browser sends/receives
// the HttpOnly session cookie set by the backend (cross-site: Vercel <-> Render).

export async function signInWithGoogle(credential: string): Promise<NicteUser> {
  const res = await fetch(`${API_URL}/v1/auth/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ credential }),
  });

  if (!res.ok) {
    throw new Error(`No se pudo iniciar sesión con Google (${res.status})`);
  }

  return res.json();
}

export async function getCurrentUser(): Promise<NicteUser | null> {
  const res = await fetch(`${API_URL}/v1/auth/me`, {
    credentials: "include",
  });

  if (!res.ok) return null;
  return res.json();
}

export async function logout(): Promise<void> {
  await fetch(`${API_URL}/v1/auth/logout`, {
    method: "POST",
    credentials: "include",
  }).catch(() => {});
}
