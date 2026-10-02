import { useEffect, useMemo, useState } from "react"
import { Link, useParams } from "react-router"
import { ArrowLeft, ArrowUpRight, Check, Clock, Link2 } from "lucide-react"
import { useArticle } from "@/hooks/queries/useArticle"

// Beberapa konten dari scraper berisi entity HTML seperti &#39; (terlihat di homepage kamu)
function decodeHtml(text: string) {
  const el = document.createElement("textarea")
  el.innerHTML = text
  return el.value
}

function formatDate(date: string | null) {
  if (!date) return null
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date))
}

function toParagraphs(text: string | null) {
  if (!text) return []
  return decodeHtml(text)
    .split(/\n+/)
    .map((p) => p.trim())
    .filter(Boolean)
}

export default function DetailArticle() {
  const { id } = useParams()
  // sesuaikan kalau signature useArticle kamu berbeda
  const { data: article, isLoading, isError } = useArticle(Number(id))

  const [showTranslated, setShowTranslated] = useState(true)
  const [copied, setCopied] = useState(false)
  const [progress, setProgress] = useState(0)

  // Progress bar baca
  useEffect(() => {
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight
      setProgress(max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0)
    }
    onScroll()
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  // Scroll ke atas saat pindah artikel
  useEffect(() => {
    window.scrollTo({ top: 0 })
  }, [id])

  const hasTranslation = Boolean(article?.translated_content || article?.translated_title)
  const useTranslated = hasTranslation && showTranslated

  const title = decodeHtml(
    (useTranslated ? article?.translated_title : article?.title) ?? article?.title ?? ""
  )
  const description = decodeHtml(
    (useTranslated ? article?.translated_description : article?.description) ??
      article?.description ??
      ""
  )
  const paragraphs = useMemo(
    () => toParagraphs(useTranslated ? article?.translated_content ?? null : article?.content ?? null),
    [article, useTranslated]
  )

  const readingTime = useMemo(() => {
    const words = paragraphs.join(" ").split(/\s+/).filter(Boolean).length
    return Math.max(1, Math.round(words / 200))
  }, [paragraphs])

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href)
      setCopied(true)
      setTimeout(() => setCopied(false), 1800)
    } catch {
      /* ignore */
    }
  }

  if (isLoading) return <ArticleSkeleton />

  if (isError || !article) {
    return (
      <div className="mx-auto flex min-h-[60vh] max-w-xl flex-col items-center justify-center px-6 text-center">
        <p className="font-serif text-5xl font-bold text-title-1st">404</p>
        <h1 className="mt-4 font-serif text-2xl font-bold text-title-1st">Article not found</h1>
        <p className="mt-2 font-sans text-sm text-body-1st">
          The article you are looking for does not exist or has been removed.
        </p>
        <Link
          to="/"
          className="mt-6 inline-flex items-center gap-2 rounded-full bg-title-1st px-5 py-2.5 font-sans text-sm font-medium text-beige-ringan transition hover:bg-title-1st/90"
        >
          <ArrowLeft className="size-4" /> Back to home
        </Link>
      </div>
    )
  }

  const published = formatDate(article.published_at)
  const byline = article.author ? decodeHtml(article.author) : null

  return (
    <>
      {/* Reading progress */}
      <div className="fixed inset-x-0 top-0 z-50 h-0.5 bg-transparent">
        <div
          className="h-full bg-title-1st transition-[width] duration-100"
          style={{ width: `${progress}%` }}
        />
      </div>

      <article className="mx-auto w-full max-w-5xl px-6 pb-24 pt-10 md:pt-14">
        {/* Back */}
        <Link
          to="/"
          className="group inline-flex items-center gap-2 font-sans text-sm text-body-1st transition hover:text-title-1st"
        >
          <ArrowLeft className="size-4 transition-transform group-hover:-translate-x-1" />
          Back to news
        </Link>

        {/* Header */}
        <header className="mx-auto mt-10 max-w-3xl text-center">
          <div className="flex items-center justify-center gap-3 font-sans text-xs font-semibold uppercase tracking-[0.18em] text-body-1st">
            {article.source_name && (
              <span className="rounded-full border border-title-1st/20 px-3 py-1 text-title-1st">
                {article.source_name}
              </span>
            )}
            {published && <span className="font-medium normal-case tracking-normal">{published}</span>}
          </div>

          <h1 className="mt-6 font-serif text-4xl font-bold leading-[1.1] tracking-tight text-title-1st md:text-6xl">
            {title}
          </h1>

          {description && (
            <p className="mx-auto mt-6 max-w-2xl font-sans text-lg leading-8 text-body-1st md:text-xl">
              {description}
            </p>
          )}
        </header>

        {/* Byline */}
        <div className="mx-auto mt-10 flex max-w-3xl flex-wrap items-center justify-between gap-4 border-y border-title-1st/15 py-4">
          <div className="font-sans text-sm">
            {byline && (
              <p className="text-body-1st">
                By <span className="font-semibold text-title-1st">{byline}</span>
              </p>
            )}
            <p className="mt-0.5 flex items-center gap-1.5 text-xs text-body-1st/80">
              <Clock className="size-3.5" /> {readingTime} min read
            </p>
          </div>

          <div className="flex items-center gap-2">
            {hasTranslation && (
              <div className="flex rounded-full border border-title-1st/15 p-0.5 font-sans text-xs font-medium">
                <button
                  onClick={() => setShowTranslated(true)}
                  className={`rounded-full px-3 py-1.5 transition ${
                    showTranslated ? "bg-title-1st text-beige-ringan" : "text-body-1st hover:text-title-1st"
                  }`}
                >
                  {article.translated_language?.toUpperCase() ?? "Translated"}
                </button>
                <button
                  onClick={() => setShowTranslated(false)}
                  className={`rounded-full px-3 py-1.5 transition ${
                    !showTranslated ? "bg-title-1st text-beige-ringan" : "text-body-1st hover:text-title-1st"
                  }`}
                >
                  Original
                </button>
              </div>
            )}

            <button
              onClick={handleCopy}
              aria-label="Copy link"
              className="flex size-9 items-center justify-center rounded-full border border-title-1st/15 text-title-1st transition hover:bg-title-1st/5"
            >
              {copied ? <Check className="size-4" /> : <Link2 className="size-4" />}
            </button>
          </div>
        </div>

        {/* Hero image */}
        <figure className="mt-10">
          <div className="overflow-hidden bg-title-1st/5">
            <img
              src={article.image_url}
              alt={title}
              className="aspect-video w-full object-cover grayscale-90 transition duration-700"
            />
          </div>
          {article.source_name && (
            <figcaption className="mt-2 text-right font-sans text-xs text-body-1st/70">
              Photo: {article.source_name}
            </figcaption>
          )}
        </figure>

        {/* Body */}
        <div className="mx-auto mt-12 max-w-2xl">
          {paragraphs.length > 0 ? (
            <div className="space-y-6 font-sans text-[1.0625rem] leading-8 text-title-1st/90">
              {paragraphs.map((p, i) => (
                <p
                  key={i}
                  className={
                    i === 0
                      ? "first-letter:float-left first-letter:mr-3 first-letter:font-serif first-letter:text-7xl first-letter:font-bold first-letter:leading-[0.8] first-letter:text-title-1st"
                      : ""
                  }
                >
                  {p}
                </p>
              ))}
            </div>
          ) : (
            <p className="text-center font-sans text-body-1st">
              The full content is not available. Please read the original article.
            </p>
          )}

          {/* Source CTA */}
          <div className="mt-14 border-t border-title-1st/15 pt-8">
            <p className="font-sans text-xs uppercase tracking-[0.18em] text-body-1st">
              Original source
            </p>
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="group mt-3 inline-flex items-center gap-2 rounded-full bg-title-1st px-6 py-3 font-sans text-sm font-medium text-beige-ringan transition hover:bg-title-1st/90"
            >
              Read on {article.source_name ?? "source website"}
              <ArrowUpRight className="size-4 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
            </a>
            <p className="mt-4 font-sans text-xs leading-5 text-body-1st/70">
              This content is aggregated from the original publisher
              {hasTranslation && " and may be machine-translated"}. Please refer to the
              source for the most accurate version.
            </p>
          </div>
        </div>
      </article>
    </>
  )
}

function ArticleSkeleton() {
  return (
    <div className="mx-auto max-w-5xl animate-pulse px-6 pt-14">
      <div className="mx-auto max-w-3xl space-y-4 text-center">
        <div className="mx-auto h-6 w-32 rounded-full bg-title-1st/10" />
        <div className="h-12 w-full rounded bg-title-1st/10" />
        <div className="mx-auto h-12 w-2/3 rounded bg-title-1st/10" />
        <div className="mx-auto h-5 w-3/4 rounded bg-title-1st/10" />
      </div>
      <div className="mt-12 aspect-video w-full bg-title-1st/10" />
      <div className="mx-auto mt-12 max-w-2xl space-y-3">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="h-4 rounded bg-title-1st/10" style={{ width: `${95 - (i % 3) * 8}%` }} />
        ))}
      </div>
    </div>
  )
}