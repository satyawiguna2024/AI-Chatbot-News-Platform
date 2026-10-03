import { useEffect, useState } from "react"
import { useLocation } from "react-router"

export function useArticleSearch() {
  const location = useLocation()

  const [searchOpen, setSearchOpen] = useState(false)
  const [searchScrolled, setSearchScrolled] = useState(false)
  const [search, setSearch] = useState("")

  const isHomePage = location.pathname === "/"

  useEffect(() => {
    if (!isHomePage) return

    const currentSearch = new URLSearchParams(location.search).get("search") ?? ""

    if (search.trim() === currentSearch.trim()) return

    const timeout = window.setTimeout(() => {
      const trimmedSearch = search.trim()
      const params = new URLSearchParams()

      if (trimmedSearch) params.set("search", trimmedSearch)

      const nextUrl = params.toString() ? `/?${params.toString()}` : "/"

      window.history.pushState({}, "", nextUrl)
      window.dispatchEvent(new PopStateEvent("popstate"))
    }, 400)

    return () => window.clearTimeout(timeout)
  }, [search, location.search, isHomePage])

  useEffect(() => {
    if (!isHomePage) return

    const searchFromUrl = new URLSearchParams(location.search).get("search") ?? ""

    // eslint-disable-next-line react-hooks/set-state-in-effect
    setSearch(searchFromUrl)
  }, [location.search, isHomePage])

  const toggleSearch = () => setSearchOpen((open) => !open)
  const handleSearchScroll = (event: React.UIEvent<HTMLInputElement>) => setSearchScrolled(event.currentTarget.scrollLeft > 0)

  return {
    search,
    searchOpen,
    searchScrolled,
    isHomePage,
    setSearch,
    toggleSearch,
    handleSearchScroll,
  }
}

