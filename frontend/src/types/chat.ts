export type ChatRole = "user" | "assistant";

export interface ChatSource {
  article_id: number;
  title: string;
  url: string;
  image_url: string | null;
  source_name: string;
}

export interface ChatMessage {
  id: string | number;
  role: ChatRole;
  content: string;
  sources?: ChatSource[] | null;
}

export interface ConversationContext {
  conversation_id: number | string | null;
  anonymous_id: string;
  article_id: number | null;
  messages: ChatMessage[];
}

export interface ConversationCreateResponse {
  conversation_id: number | string;
  anonymous_id: string;
  article_id: number | null;
}

export interface ChatRequestPayload {
  anonymous_id: string;
  article_id: number | null;
  question: string;
}

export type ChatStreamEvent =
  | { type: "token"; content: string }
  | { type: "sources"; sources: ChatSource[] }
  | { type: "done" }
  | { type: "error"; message?: string };