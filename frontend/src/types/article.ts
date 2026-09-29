export interface ArticleListItem {
  id: number
  title: string
  translated_title: string | null
  description: string | null
  translated_description: string | null
  source_name: string | null
  author: string | null
  published_at: string | null
  image_url: string
  url: string
}

export interface ArticleListResponse {
  items: ArticleListItem[]
  page: number
  limit: number
  total: number
  total_pages: number
  has_next: boolean
}

export interface ArticleDetail {
  id: number
  title: string
  description: string | null
  content: string | null

  translated_title: string | null
  translated_description: string | null
  translated_content: string | null
  translated_language: string | null

  source_name: string | null
  author: string | null
  published_at: string | null
  image_url: string
  url: string
  created_at: string
}