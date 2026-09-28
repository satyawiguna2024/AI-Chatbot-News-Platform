import { useArticles } from "@/hooks/queries/useArticles";
import { Link } from "react-router";

export default function TrendingArticle() {
  const { data } = useArticles(20, 3)

  return (
    <>
      <div className="my-container px-4 py-2">
        <h1 className="font-sans font-extrabold text-2xl xs:text-3xl underline decoration-2 underline-offset-4 mt-16 sm:mt-36 mb-20 text-end">
          Trending Article
        </h1>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
          {data?.items?.slice(0, 3).map((article, i) => (
            <div
              key={i}
              className="relative flex flex-col justify-center pr-0 sm:pr-5 border-gray-300"
            >
              <Link
                to="/"
                className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
              >
                {/* image */}
                <div className="mb-3 overflow-hidden shadow-md">
                  <img
                    src={article.image_url}
                    alt={article.title}
                    className="h-auto w-full grayscale-90 transition-transform duration-500 ease-out md:group-hover:scale-[1.025]"
                  />
                </div>

                <span className="flex justify-between mb-5">
                  <span className="font-sans text-xs font-medium text-body-1st max-w-45 md:max-w-30 lg:max-w-45 truncate">
                    By {article.author}
                  </span>
                  <span className="font-sans text-xs font-medium text-body-1st">
                    17-08-1945
                  </span>
                </span>

                <h1 className="mb-3 font-serif text-xl font-extrabold max-w-auto leading-7 md:text-2xl md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4 line-clamp-2">
                  {article.title}
                </h1>

                <p className="font-sans text-sm text-black font-light mb-5 sm:max-w-77.5 lg:max-w-90 leading-relaxed line-clamp-3">
                  {article.description}
                </p>
              </Link>

              {i < 2 && (
                <div className="absolute right-0 top-0 h-full w-px bg-gray-300 hidden sm:block" />
              )}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}