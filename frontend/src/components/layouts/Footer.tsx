import { Link } from "react-router"
import IconAskNews from "@/assets/icons/icon-asknews.png"

export default function Footer() {
  return (
    <footer className="mt-14 border-t border-gray-300">
      <div className="my-container px-4 py-10 text-center md:py-14">
        <div className="flex flex-col items-center">
          {/* Brand */}
          <Link
            to="/"
            className="group inline-block"
          >
            <img src={IconAskNews} alt="Icon Ask News" className="size-30 mx-auto" />
            <h1 className="font-serif text-4xl font-extrabold tracking-tight transition-all duration-300 group-hover:underline group-hover:decoration-1 group-hover:underline-offset-4 md:text-5xl">
              Ask News
            </h1>
          </Link>

          {/* Description */}
          <p className="mt-5 max-w-md font-sans text-sm font-light leading-relaxed text-body-1st md:text-base">
            Independent stories, current events, and conversations
            presented with clarity.
          </p>
        </div>

        {/* Divider */}
        <div className="my-8 border-t border-gray-300" />

        {/* Bottom footer */}
        <div className="flex justify-center">
          {/* Copyright */}
          <span className="font-sans text-xs font-medium text-body-1st">
            © 2026 Ask News. All rights reserved.
          </span>
        </div>
      </div>
    </footer>
  )
}