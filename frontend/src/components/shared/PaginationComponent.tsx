import { Pagination, PaginationContent, PaginationEllipsis, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "@/components/ui/pagination"
import type { PaginationComponentProps } from "@/types/pagination"
import { getPageNumbers, getCompactPageNumbers } from "@/lib/pagination"

export function PaginationComponent({ page, totalPages, onPageChange }: PaginationComponentProps) {
  const canGoPrevious = page > 1
  const canGoNext = page < totalPages
  const pageNumbers = getPageNumbers(page, totalPages)
  const compactPageNumbers = getCompactPageNumbers(page, totalPages)

  if (totalPages <= 0) return null

  return (
    <Pagination>
      <PaginationContent className="gap-1 max-[500px]:gap-0">
        <PaginationItem>
          <PaginationPrevious
            aria-disabled={!canGoPrevious}
            className="font-sans text-body-1st transition-colors duration-200 hover:bg-[#E5DFD2] hover:text-title-1st aria-disabled:pointer-events-none aria-disabled:opacity-40 max-[500px]:gap-0 max-[500px]:px-2 max-[500px]:[&>span]:hidden"
            onClick={(event) => {
              event.preventDefault()
              if (canGoPrevious) onPageChange(page - 1)
            }}
          />
        </PaginationItem>

        <div className="hidden items-center gap-1 min-[501px]:flex">
          {pageNumbers[0] > 1 && (
            <>
              <PaginationItem>
                <PaginationLink
                  onClick={(event) => {
                    event.preventDefault()
                    onPageChange(1)
                  }}
                  className="font-sans text-body-1st transition-colors duration-200 hover:bg-[#E5DFD2] hover:text-title-1st"
                >
                  1
                </PaginationLink>
              </PaginationItem>

              <PaginationItem>
                <PaginationEllipsis className="text-body-2nd" />
              </PaginationItem>
            </>
          )}

          {pageNumbers.map((pageNumber) => (
            <PaginationItem key={pageNumber}>
              <PaginationLink
                isActive={pageNumber === page}
                onClick={(event) => {
                  event.preventDefault()
                  onPageChange(pageNumber)
                }}
                className="font-sans text-body-1st transition-colors duration-200 hover:bg-[#E5DFD2] hover:text-title-1st data-[active=true]:border-title-1st data-[active=true]:bg-title-1st data-[active=true]:text-beige-ringan data-[active=true]:hover:bg-[#333333] data-[active=true]:hover:text-beige-ringan"
              >
                {pageNumber}
              </PaginationLink>
            </PaginationItem>
          ))}

          {pageNumbers[pageNumbers.length - 1] < totalPages && (
            <>
              <PaginationItem>
                <PaginationEllipsis className="text-body-2nd" />
              </PaginationItem>

              <PaginationItem>
                <PaginationLink
                  onClick={(event) => {
                    event.preventDefault()
                    onPageChange(totalPages)
                  }}
                  className="font-sans text-body-1st transition-colors duration-200 hover:bg-[#E5DFD2] hover:text-title-1st"
                >
                  {totalPages}
                </PaginationLink>
              </PaginationItem>
            </>
          )}
        </div>

        <div className="flex items-center gap-0 min-[501px]:hidden">
          {compactPageNumbers.map((item, index) => {
            if (item === "ellipsis") {
              return (
                <PaginationItem key={`ellipsis-${index}`}>
                  <PaginationEllipsis className="text-body-2nd max-[500px]:size-7" />
                </PaginationItem>
              )
            }

            return (
              <PaginationItem key={item}>
                <PaginationLink
                  isActive={item === page}
                  onClick={(event) => {
                    event.preventDefault()
                    onPageChange(item)
                  }}
                  className="size-8 font-sans text-sm text-body-1st transition-colors duration-200 hover:bg-[#E5DFD2] hover:text-title-1st data-[active=true]:border-title-1st data-[active=true]:bg-title-1st data-[active=true]:text-beige-ringan data-[active=true]:hover:bg-[#333333] data-[active=true]:hover:text-beige-ringan max-[500px]:size-7"
                >
                  {item}
                </PaginationLink>
              </PaginationItem>
            )
          })}
        </div>

        <PaginationItem>
          <PaginationNext
            aria-disabled={!canGoNext}
            className="font-sans text-body-1st transition-colors duration-200 hover:bg-[#E5DFD2] hover:text-title-1st aria-disabled:pointer-events-none aria-disabled:opacity-40 max-[500px]:gap-0 max-[500px]:px-2 max-[500px]:[&>span]:hidden"
            onClick={(event) => {
              event.preventDefault()
              if (canGoNext) onPageChange(page + 1)
            }}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  )
}