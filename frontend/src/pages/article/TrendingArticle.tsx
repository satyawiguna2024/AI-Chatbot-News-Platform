import { Link } from "react-router";

export default function TrendingArticle() {
  return (
    <>
      <div className="my-container px-4 py-2">
        <h1 className="font-sans font-extrabold text-2xl xs:text-3xl underline decoration-2 underline-offset-4 mt-16 sm:mt-36 mb-20">Trending Article</h1>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <div
              key={i}
              className="relative flex flex-col justify-center pr-0 sm:pr-5 border-gray-300"
            >
              <Link to="/">
                <img
                  src="https://images.unsplash.com/photo-1790108931626-f26b56184fb8?q=80&w=1740&auto=format&fit=crop"
                  alt="Unsplash"
                  className="mb-3 h-auto w-full shadow-md grayscale-90"
                />

                <h1 className="mb-3 font-serif text-xl md:text-2xl font-extrabold max-w-100 leading-7">
                  Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ratione,
                  maxime?
                </h1>

                <p className="font-sans text-sm text-black font-light mb-5 sm:max-w-77.5 lg:max-w-90 leading-relaxed">
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt totam illum, at repellendus saepe laboriosam natus ipsam sequi facilis dolore corrupti cupiditate molestias? Amet animi hic debitis eveniet autem. Pariatur.
                </p>

                {/* author */}
                <span className="font-sans text-xs font-medium underline sm:mb-5">By Hils</span>
              </Link>

              {i < 2 && (
                <div className="absolute right-0 top-0 h-full w-px bg-gray-300 hidden sm:block" />
              )}
            </div>
          ))}
        </div>
      </div>
    </>
  )
}
