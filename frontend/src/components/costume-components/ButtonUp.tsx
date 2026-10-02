import { useEffect, useState } from "react"
import { ArrowUp } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function ButtonUp() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 300)
    onScroll()
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  return (
    <>
      <Button
        type="button"
        variant="outline"
        size="icon"
        aria-label="Scroll to top"
        onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
        className={`
          fixed left-5 bottom-8 z-50 size-13 rounded-full border-title-1st/40 bg-beige-ringan text-title-1st shadow-[0_3px_10px_rgba(26,26,26,0.10),0_8px_24px_rgba(26,26,26,0.08)] transition-all duration-300 ease-out hover:scale-105 hover:border-title-1st/60 hover:bg-beige-ringan hover:shadow-[0_4px_12px_rgba(26,26,26,0.12),0_10px_28px_rgba(26,26,26,0.12)] active:scale-95 xl:size-14
          ${visible ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-4 opacity-0"}
        `}
        >
        <ArrowUp className="size-6 stroke-[1.8]" />
      </Button>
    </>
  )
}