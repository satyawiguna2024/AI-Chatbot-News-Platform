import { useQuery } from "@tanstack/react-query"
import { getArticle } from "@/lib/api/articles"

export function useArticle(articleId: number) {
  return useQuery({
    queryKey: ["article", articleId],
    queryFn: () => getArticle(articleId),
    enabled: articleId > 0,
  })
}