import { useEffect, useState } from "react"

const STEPS_ROOT = [
  "Thinking...",
  "Understanding your question...",
  "Searching through articles...",
  "Reading the most relevant results...",
  "Preparing your answer...",
]

const STEPS_ARTICLE = [
  "Reading this article...",
  "Finding the relevant parts...",
  "Preparing your answer...",
]

export function ThinkingStatus({ isArticle }: { isArticle: boolean }) {
  const steps = isArticle ? STEPS_ARTICLE : STEPS_ROOT
  const [index, setIndex] = useState(0)

  useEffect(() => {
    // berhenti di langkah terakhir, tidak mengulang dari awal
    if (index >= steps.length - 1) return
    const timer = setTimeout(() => setIndex((i) => i + 1), 2200)
    return () => clearTimeout(timer)
  }, [index, steps.length])

  return (
    <span className="flex items-center gap-2 text-body-1st/60">
      <span className="flex gap-0.5">
        <span className="size-1 animate-bounce rounded-full bg-body-1st/50 [animation-delay:-0.3s]" />
        <span className="size-1 animate-bounce rounded-full bg-body-1st/50 [animation-delay:-0.15s]" />
        <span className="size-1 animate-bounce rounded-full bg-body-1st/50" />
      </span>
      <span key={index} className="animate-pulse">{steps[index]}</span>
    </span>
  )
}