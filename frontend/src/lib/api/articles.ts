import { apiClient } from "@/lib/api/client"
import type {ArticleListResponse, ArticleDetail} from "@/types/article"

export function getArticles(page = 1, limit = 12) {
  return apiClient<ArticleListResponse>(`/articles?page=${page}&limit=${limit}`)
}

export function getArticle(articleId: number) {
  return apiClient<ArticleDetail>(`/articles/${articleId}`)
}