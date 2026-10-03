import { Link } from "react-router"
import { Separator } from "@/components/ui/separator"
import { Toggle } from "@/components/ui/toggle"
import { Search } from "lucide-react"
import { useLanguage } from "@/hooks/useLanguage"
import IconAskNews from "@/assets/icons/icon-asknews.png"
import { useNavbarScroll } from "@/hooks/useNavbarScroll"
import { useArticleSearch } from "@/hooks/useArticleSearch"

export default function Navbar() {
  const { language, setLanguage } = useLanguage()
  const { isScrolled } = useNavbarScroll()
  const { search, searchOpen, searchScrolled, isHomePage, setSearch, toggleSearch, handleSearchScroll, } = useArticleSearch()
  const handleLanguageChange = (pressed: boolean) => { setLanguage(pressed ? "id" : "en") }

  return (
    <nav
      className={`
        sticky top-0 z-50 w-full transition-all duration-300 ease-out
        ${isScrolled ? "border-b border-title-1st/10 bg-beige-ringan/90 shadow-[0_4px_16px_rgba(26,26,26,0.04)] backdrop-blur-sm" : "border-b border-transparent bg-transparent"}
      `}
    >
      <div className={`my-container px-4 transition-[padding] duration-300 ease-out ${isScrolled ? "py-1" : "py-2"}`}>
        <div className="flex items-center justify-between">
          <Link to="/" className="-ml-3 flex items-center">
            <img
              src={IconAskNews}
              alt="Icon AskNews"
              className={`transition-[width,height] duration-300 ease-out ${isScrolled ? "size-10 md:size-11 lg:size-13" : "size-11 md:size-12 lg:size-15"}`}
            />

            <h1
              className={`
                font-sans text-md text-nowrap font-bold tracking-wide text-title-1st transition-all duration-300 sm:text-[17px] md:text-lg lg:text-2xl
                ${searchOpen ? "hidden xs:block" : ""}
                ${isScrolled ? "md:tracking-[0.015em]" : ""}
              `}
            >
              Ask News
            </h1>
          </Link>

          <div className="hidden sm:block">
            <h1 className=" font-sans text-sm font-bold tracking-wide text-title-1st lg:text-md">
              example.asknews@gmail.com
            </h1>
          </div>

          <div className="flex items-center gap-2">
            {isHomePage && (
              <div
                className={`
                  flex items-center overflow-hidden rounded-md transition-[width,border-color,background-color] duration-300 ease-out
                  ${searchOpen ? "w-36 border border-title-1st/30 bg-beige-ringan/40 px-1 sm:w-44 md:w-52" : "w-6 border border-transparent bg-transparent"}
                `}
              >
                {/* Search button */}
                <button
                  type="button"
                  aria-label={searchOpen ? "Close search" : "Open search"}
                  onClick={toggleSearch}
                  className="flex size-6 shrink-0 items-center justify-center"
                >
                  <Search className="size-4.5 stroke-[2.5] transition-transform duration-200 sm:size-5 md:size-5.25 lg:size-5.75" />
                </button>

                {/* Search input */}
                <div className="relative min-w-0 flex-1">
                  <input
                    type="text"
                    value={search}
                    onChange={(event) => setSearch(event.target.value)}
                    onScroll={handleSearchScroll}
                    placeholder={language === "id" ? "Cari Artikel..." : "Search Article..."}
                    className={`
                      w-full min-w-0 bg-transparent px-2 py-0 font-sans text-sm text-title-1st outline-none transition-opacity duration-200 lg:py-2
                      ${searchOpen ? "opacity-100" : "pointer-events-none opacity-0"}
                    `}
                  />

                  {searchScrolled && (
                    <div className=" pointer-events-none absolute inset-y-0 left-0 w-6 bg-linear-to-r from-title-1st/5 to-transparent" />
                  )}
                </div>
              </div>
            )}


            <Separator orientation="vertical" className="ml-1 -mr-2 bg-title-1st" />

            <Toggle
              pressed={language === "id"}
              onPressedChange={handleLanguageChange}
              variant="noneVariant"
              className="font-sans text-md font-bold uppercase tracking-wide text-title-1st transition-opacity duration-200 sm:text-md md:text-lg lg:text-xl"
            >
              {language}
            </Toggle>
          </div>
        </div>
      </div>
    </nav>
  )
}