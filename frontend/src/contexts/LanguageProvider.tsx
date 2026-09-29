import { useState } from "react"
import { LanguageContext } from "./LanguageContext"
import type { Language } from "./LanguageContext"


export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguage] = useState<Language>("en")

  return (
    <LanguageContext.Provider value={{ language, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  )
}