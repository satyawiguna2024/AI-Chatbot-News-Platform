import { useQuery } from "@tanstack/react-query";
import { getArticles } from "@/lib/api/articles";

const FETCH_LIMIT = 98;

export function useArticles() {
  return useQuery({
    queryKey: ["articles"],
    queryFn: () => getArticles(1, FETCH_LIMIT),
    staleTime: 5 * 60 * 1000,
  });
}
