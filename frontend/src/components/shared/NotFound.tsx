import { ArrowLeft } from "lucide-react";
import { Link } from "react-router";

export default function NotFound({title, description}: {title?: string; description?: string}) {
  return (
    <div className="mx-auto flex min-h-screen max-w-xl flex-col items-center justify-center px-6 text-center">
      <p className="font-serif text-5xl font-bold text-title-1st">404</p>
      <h1 className="mt-4 font-serif text-2xl font-bold text-title-1st">{title}</h1>
      <p className="mt-2 font-sans text-sm text-body-1st">
        {description}
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