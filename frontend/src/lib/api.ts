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
