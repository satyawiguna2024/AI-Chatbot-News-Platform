import { useState } from "react"
import { Link } from "react-router"
import { Separator } from "@/components/ui/separator"
import { Toggle } from "@/components/ui/toggle"
import { Search } from "lucide-react"
import { useLanguage } from "@/hooks/useLanguage"
import IconAskNews from "@/assets/icons/icon-asknews.png"

export default function Navbar() {
  const [searchOpen, setSearchOpen] = useState(false)
  const [searchScrolled, setSearchScrolled] = useState(false)
  const [search, setSearch] = useState("")
  const { language, setLanguage } = useLanguage()

  return (
    <nav className="my-container px-4 py-2">
      <div className="flex items-center justify-between">
        {/* Logo & Title */}
        <Link
          to="/"
          className="-ml-3 flex items-center"
        >
          <img src={IconAskNews} alt="Icon AskNews" className="size-11 md:size-12 lg:size-15" />

          <h1
            className={`
              font-sans text-md text-nowrap font-bold tracking-wide text-title-1st sm:text-[17px] md:text-lg lg:text-2xl
              ${searchOpen && "hidden xs:block"}
            `}
          >
            Ask News
          </h1>
        </Link>

        <div className="hidden sm:block">
          <h1 className="font-sans text-sm lg:text-md font-bold tracking-wide text-title-1st">
            example.asknews@gmail.com
          </h1>
        </div>

        <div className="flex items-center gap-2">
          {/* Search */}
          <div
            className={`
              flex items-center overflow-hidden rounded-md
              transition-[width,border-color]
              duration-300 ease-out
              ${searchOpen
                ? "w-36 border border-title-1st/30 sm:w-44 md:w-52 px-1"
                : "w-6 border border-transparent"
              }
            `}
          >
            <button
              type="button"
              aria-label={searchOpen ? "Close search" : "Open search"}
              onClick={() => setSearchOpen((open) => !open)}
              className="flex size-6 shrink-0 items-center justify-center"
            >
              <Search className="size-4.5 stroke-[2.5] sm:size-5 md:size-5.25 lg:size-5.75" />
            </button>

            <div className="relative min-w-0 flex-1">
              <input
                type="text"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search..."
                onScroll={(event) => {
                  setSearchScrolled(event.currentTarget.scrollLeft > 0)
                }}
                className={`
                  w-full min-w-0 bg-transparent px-2 py-0 lg:py-2
                  font-sans text-sm text-title-1st
                  outline-none
                  transition-opacity duration-200
                  ${searchOpen ? "opacity-100" : "pointer-events-none opacity-0"}
                `}
              />

              {searchScrolled && (
                <div className=" pointer-events-none absolute inset-y-0 left-0 w-6 bg-linear-to-r from-black/5 to-transparent" />
              )}
            </div>
          </div>

          {/* Separator */}
          <Separator orientation="vertical" className="bg-title-1st ml-1 -mr-2" />

          {/* Language */}
          <Toggle
            pressed={language === "id"}
            onPressedChange={(pressed) =>
              setLanguage(pressed ? "id" : "en")
            }
            variant="noneVariant"
            className="font-sans text-md font-bold uppercase tracking-wide text-title-1st sm:text-md md:text-lg lg:text-xl"
          >
            {language}
          </Toggle>
        </div>
      </div>
    </nav>
  )
}