import type {
  ChatRequestPayload,
  ChatStreamEvent,
  ConversationContext,
  ConversationCreateResponse,
} from "@/types/chat";

const API_URL = import.meta.env.VITE_API_BASE_URL

export class ChatQuotaError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ChatQuotaError";
  }
}

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `Request gagal (${res.status})`);
  }
  return res.json() as Promise<T>;
}

export async function getConversationContext(
  anonymousId: string,
  articleId: number | null
): Promise<ConversationContext> {
  const params = new URLSearchParams({ anonymous_id: anonymousId });
  if (articleId !== null) params.set("article_id", String(articleId));
  return json(await fetch(`${API_URL}/conversation/context?${params}`));
}

export async function createConversation(payload: {
  anonymous_id: string;
  article_id: number | null;
}): Promise<ConversationCreateResponse> {
  return json(
    await fetch(`${API_URL}/conversation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
}

export async function deleteConversation(payload: { anonymous_id: string }) {
  return json<{ status: string }>(
    await fetch(`${API_URL}/conversation`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
}

export async function streamChat(params: {
  payload: ChatRequestPayload;
  signal?: AbortSignal;
  onEvent: (event: ChatStreamEvent) => void;
}): Promise<{ remaining: number | null }> {
  const { payload, signal, onEvent } = params;

  const res = await fetch(`${API_URL}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal,
  });

  if (res.status === 429) {
    const body = await res.json().catch(() => null);
    throw new ChatQuotaError(body?.detail ?? "Kuota chat kamu sudah habis.");
  }
  if (!res.ok || !res.body) {
    throw new Error(`Chat gagal (${res.status})`);
  }

  // butuh expose_headers di CORS backend, kalau tidak hasilnya null
  const header = res.headers.get("X-RateLimit-Remaining");
  const remaining = header !== null ? Number(header) : null;

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split("\n\n");
    buffer = chunks.pop() ?? "";

    for (const chunk of chunks) {
      const line = chunk.split("\n").find((l) => l.startsWith("data: "));
      if (!line) continue;
      try {
        onEvent(JSON.parse(line.slice(6)) as ChatStreamEvent);
      } catch {
        /* abaikan chunk yang rusak */
      }
    }
  }

  return { remaining };
}