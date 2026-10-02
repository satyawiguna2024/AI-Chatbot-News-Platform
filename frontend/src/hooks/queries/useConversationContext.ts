import { useQuery } from "@tanstack/react-query";
import { getConversationContext } from "@/lib/api/chat";

export const chatKeys = {
  all: ["conversation"] as const,
  context: (anonymousId: string, articleId: number | null) =>
    ["conversation", "context", anonymousId, articleId] as const,
};

// opsional, kalau mau dipakai langsung di komponen
export function useConversationContext(
  anonymousId: string,
  articleId: number | null,
  enabled = true
) {
  return useQuery({
    queryKey: chatKeys.context(anonymousId, articleId),
    queryFn: () => getConversationContext(anonymousId, articleId),
    enabled,
  });
}