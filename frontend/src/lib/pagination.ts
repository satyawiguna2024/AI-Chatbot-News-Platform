import type { PageItem } from "@/types/pagination"

export function getPageNumbers(page: number, totalPages: number): number[] {
  const maxVisiblePages = 5

  if (totalPages <= maxVisiblePages) return Array.from({ length: totalPages }, (_, index) => index + 1)
  if (page <= 3) return [1, 2, 3, 4, 5]
  if (page >= totalPages - 2) return [totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages]

  return [ page - 2, page - 1, page, page + 1, page + 2]
}

export function getCompactPageNumbers(page: number, totalPages: number): PageItem[] {
  if (totalPages <= 4) return Array.from({ length: totalPages }, (_, index) => index + 1)
  if (page <= 2) return [1, 2, 3, "ellipsis", totalPages]
  if (page >= totalPages - 1) return [1, "ellipsis", totalPages - 2, totalPages - 1, totalPages]

  return [1, "ellipsis", page, "ellipsis", totalPages]
}