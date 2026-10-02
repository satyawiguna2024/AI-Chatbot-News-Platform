import { Link } from "react-router"
import type { ChatSource } from "@/types/chat"

type SourceCardsProps = {
  sources?: ChatSource[] | null
  onNavigate?: () => void // dipakai untuk menutup modal saat kartu diklik
}

export function SourceCards({ sources, onNavigate }: SourceCardsProps) {
  if (!sources || sources.length === 0) return null

  return (
    <div className="mt-2 flex flex-col gap-2">
      {sources.map((source) => (
        <Link
          key={source.article_id}
          to={`/article/${source.article_id}/detail`} // sesuaikan dengan route kamu
          onClick={onNavigate}
          className="flex gap-3 overflow-hidden rounded-xl border border-title-1st/10 bg-title-1st/5 p-2 transition hover:bg-title-1st/10"
        >
          {source.image_url && (
            <img
              src={source.image_url}
              alt=""
              className="size-14 shrink-0 rounded-lg object-cover"
              loading="lazy"
            />
          )}
          <div className="min-w-0">
            <p className="line-clamp-2 font-sans text-xs font-medium text-title-1st">
              {source.title}
            </p>
            <p className="mt-1 font-sans text-[10px] text-body-1st/60">
              {source.source_name}
            </p>
          </div>
        </Link>
      ))}
    </div>
  )
}