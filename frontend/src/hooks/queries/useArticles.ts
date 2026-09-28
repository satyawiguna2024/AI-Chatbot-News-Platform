import { useQuery } from "@tanstack/react-query"
import { getArticles } from "@/lib/api/articles"

export function useArticles(page = 1, limit = 12) {
  return useQuery({
    queryKey: ["articles", page, limit],
    queryFn: () => getArticles(page, limit),
  })
}