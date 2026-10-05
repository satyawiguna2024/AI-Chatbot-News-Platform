import { useQuery } from "@tanstack/react-query";
import { getArticle } from "@/lib/api/articles";

export function useArticle(id: number) {
  return useQuery({
    queryKey: ["article", id],
    queryFn: () => getArticle(id),
    enabled: id > 0,
    retry: false,
    staleTime: 5 * 60 * 1000,
  });
}
