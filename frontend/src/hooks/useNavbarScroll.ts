
import { useEffect, useState } from "react"

export function useNavbarScroll() {
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 8)
    handleScroll()
    window.addEventListener("scroll", handleScroll, { passive: true, })
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return { isScrolled }
}
