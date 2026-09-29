import { useEffect, useMemo } from "react"
import { Link, useSearchParams } from "react-router"

import { PaginationComponent } from "@/components/costume-components/PaginationComponent"
import { useArticles } from "@/hooks/queries/useArticles"
import { useLanguage } from "@/hooks/useLanguage"

export default function ListArticles() {
  const { language } = useLanguage()
  const [searchParams, setSearchParams] = useSearchParams()
  const searchQuery = searchParams.get("search") ?? ""
  const pageParam = Number(searchParams.get("page")) || 1
  const page = Math.max(1, pageParam)
  const pageSize = 10
  const { data, isLoading, isError } = useArticles()

  useEffect(() => {
    if (!searchQuery.trim()) return

    const articlesSection = document.getElementById("articles")

    if (!articlesSection) return

    articlesSection.scrollIntoView({ behavior: "smooth", block: "start" })
  }, [searchQuery])

  const filteredArticles = useMemo(() => {
    const articles = data?.items ?? []

    if (!searchQuery.trim()) return articles

    const normalizedSearch = searchQuery.trim().toLowerCase()

    return articles.filter(
      (article) => {
        const title = language === "id" ? article.translated_title : article.title
        const description = language === "id" ? article.translated_description : article.description
        const normalizedTitle = title?.toLowerCase() ?? ""
        const normalizedDescription = description?.toLowerCase() ?? ""

        return (normalizedTitle.includes(normalizedSearch) || normalizedDescription.includes(normalizedSearch)
        )
      },
    )
  }, [data?.items, searchQuery, language])

  const totalPages = Math.ceil(filteredArticles.length / pageSize)

  const paginatedArticles = useMemo(() => {
    const startIndex = (page - 1) * pageSize
    const endIndex = startIndex + pageSize

    return filteredArticles.slice(startIndex, endIndex)
  }, [filteredArticles, page])

  const handlePageChange = (nextPage: number) => {
    const params = new URLSearchParams(searchParams)

    if (nextPage === 1) {
      params.delete("page")
    } else {
      params.set("page", String(nextPage))
    }

    setSearchParams(params)
    const articlesSection = document.getElementById("articles")

    if (!articlesSection) return

    articlesSection.scrollIntoView({ behavior: "smooth", block: "start" })
  }

  return (
    <div id="articles" className="my-container scroll-mt-24 px-4 py-2">
      <h1 className="mt-16 mb-20 font-sans text-2xl font-extrabold underline decoration-2 underline-offset-4 xs:text-3xl sm:mt-36">
        {language === "id" ? "Artikel" : "Article"}
      </h1>

      {isLoading && (
        <div className="mb-20 font-sans text-sm">
          {language === "id"
            ? "Memuat artikel..."
            : "Loading articles..."}
        </div>
      )}

      {isError && (
        <div className="mb-20 font-sans text-sm">
          {language === "id" ? "Gagal memuat artikel." : "Failed to load articles."}
        </div>
      )}

      {!isLoading && !isError && paginatedArticles.length === 0 && (
        <div className="mb-20 font-sans text-sm">
          {searchQuery.trim()
            ? language === "id" ? "Artikel tidak ditemukan." : "No articles found."
            : language === "id" ? "Belum ada artikel." : "No articles available."
          }
        </div>
      )}


      {!isLoading && !isError && paginatedArticles.length > 0 && (
        <>
          <div className="mb-30 grid grid-cols-2 gap-5 xs:grid-cols-3 md:grid-cols-4 xl:grid-cols-5">
            {paginatedArticles.map(
              (article) => (
                <div key={article.id} className="relative flex flex-col justify-center border-gray-300 pr-0 sm:pr-5">
                  <Link
                    to={`/article/${article.id}/detail`}
                    className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                  >
                    {/* Image */}
                    <div className="mb-3 overflow-hidden shadow-md">
                      <img
                        src={article.image_url}
                        alt={article.title}
                        className="h-auto w-full grayscale-90 transition-[transform,filter,box-shadow] duration-500 ease-out group-hover:scale-[1.025] group-hover:shadow-lg"
                      />
                    </div>

                    {/* Author + Date */}
                    <span className="mb-4 flex justify-between">
                      <span className="max-w-12.5 truncate font-sans text-[11px] font-medium text-body-1st sm:max-w-17.5">
                        By {article.author}
                      </span>

                      <span className="font-sans text-[11px] font-medium text-body-1st">
                        {article.published_at ? new Date(article.published_at).toLocaleDateString(language === "id" ? "id-ID" : "en-US") : "-"}
                      </span>
                    </span>

                    <h2 className=" mb-3 line-clamp-2 font-serif text-[15px] font-extrabold leading-4 transition-[text-decoration] duration-300 group-hover:underline group-hover:decoration-1 group-hover:underline-offset-4 md:text-lg md:leading-5">
                      {language === "id" ? article.translated_title : article.title}
                    </h2>
                  </Link>
                </div>
              ),
            )}
          </div>


          {totalPages > 1 && (
            <PaginationComponent
              page={page}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          )}
        </>
      )}
    </div>
  )
}