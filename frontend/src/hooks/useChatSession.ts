import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { getAnonymousId, getLastScope, setLastScope } from "@/lib/anonymous";
import { ChatQuotaError, getConversationContext, streamChat } from "@/lib/api/chat";
import { chatKeys } from "@/hooks/queries/useConversationContext";
import { useCreateConversation, useDeleteConversation } from "@/hooks/mutations/useConversationMutations";
import type { ChatMessage } from "@/types/chat";

// mencegah proses ensure jalan dobel (React StrictMode / klik modal berulang)
const inflight = new Map<string, Promise<ChatMessage[]>>();

interface Options {
  open: boolean;
  articleId: number | null; // null = root/public, angka = detail artikel
}

export function useChatSession({ open, articleId }: Options) {
  const qc = useQueryClient();
  const anonymousId = useMemo(() => getAnonymousId(), []);
  const scope = articleId === null ? "root" : String(articleId);

  const { mutateAsync: createAsync } = useCreateConversation();
  const { mutateAsync: deleteAsync } = useDeleteConversation();

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isReady, setIsReady] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [remaining, setRemaining] = useState<number | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  // 1. Siapkan conversation setiap modal dibuka / scope berubah
  useEffect(() => {
    if (!open) return;

    let cancelled = false;
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setIsReady(false);
    setError(null);

    const run = async (): Promise<ChatMessage[]> => {
      // pindah scope -> hapus conversation lama dulu (harus selesai sebelum create)
      const last = getLastScope();
      if (last && last !== scope) {
        await deleteAsync({ anonymous_id: anonymousId });
        qc.removeQueries({ queryKey: chatKeys.all });
      }

      const ctx = await qc.fetchQuery({
        queryKey: chatKeys.context(anonymousId, articleId),
        queryFn: () => getConversationContext(anonymousId, articleId),
        staleTime: 0,
      });

      // belum ada conversation -> buat. Sudah ada -> pakai yang lama
      if (!ctx.conversation_id) {
        await createAsync({ anonymous_id: anonymousId, article_id: articleId });
      }

      setLastScope(scope);
      return ctx.messages ?? [];
    };

    let promise = inflight.get(scope);
    if (!promise) {
      promise = run().finally(() => inflight.delete(scope));
      inflight.set(scope, promise);
    }

    promise
      .then((history) => {
        if (cancelled) return;
        setMessages(history);
        setIsReady(true);
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message);
      });

    return () => {
      cancelled = true;
      abortRef.current?.abort(); // hentikan stream kalau scope berubah / modal ditutup
    };
  }, [open, scope, articleId, anonymousId, qc, createAsync, deleteAsync]);

  // 2. Kirim pertanyaan + baca stream
  const send = useCallback(
    async (question: string) => {
      const q = question.trim();
      if (!q || !isReady || isStreaming) return;

      const assistantId = crypto.randomUUID();
      setError(null);
      setIsStreaming(true);
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "user", content: q },
        { id: assistantId, role: "assistant", content: "", sources: null },
      ]);

      const controller = new AbortController();
      abortRef.current = controller;

      try {
        const { remaining } = await streamChat({
          payload: { anonymous_id: anonymousId, article_id: articleId, question: q },
          signal: controller.signal,
          onEvent: (event) => {
            if (event.type === "token") {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId ? { ...m, content: m.content + event.content } : m
                )
              );
            } else if (event.type === "sources") {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId ? { ...m, sources: event.sources } : m
                )
              );
            } else if (event.type === "error") {
              setError(event.message ?? "Terjadi kesalahan pada chatbot.");
            }
          },
        });
        setRemaining(remaining);
      } catch (e) {
        if ((e as Error).name === "AbortError") return;
        // buang bubble assistant yang kosong
        setMessages((prev) => prev.filter((m) => m.id !== assistantId));
        setError(
          e instanceof ChatQuotaError ? e.message : "Gagal mengirim pesan, coba lagi."
        );
      } finally {
        setIsStreaming(false);
      }
    },
    [anonymousId, articleId, isReady, isStreaming]
  );

  return { messages, isReady, isStreaming, error, remaining, send };
}