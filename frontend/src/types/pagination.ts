export type PaginationComponentProps = {
  page: number
  totalPages: number
  onPageChange: (page: number) => void
}

export type PageItem = number | "ellipsis"