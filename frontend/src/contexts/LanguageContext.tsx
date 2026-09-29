import { createContext } from "react"

export type Language = "en" | "id"
export type LanguageContextType = {
  language: Language
  setLanguage: (language: Language) => void
}

export const LanguageContext = createContext<LanguageContextType | null>(null)