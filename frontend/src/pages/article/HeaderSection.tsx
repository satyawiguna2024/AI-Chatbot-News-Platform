import { useArticles } from "@/hooks/queries/useArticles"
import { Separator } from "@/components/ui/separator"
import { Link } from "react-router"
import { useLanguage } from "@/hooks/useLanguage"

export default function HeaderSection() {
  const { data } = useArticles()
  const { language } = useLanguage()
  const articles = data?.items ?? []

  const mainArticle = articles[0]
  const leftTopArticle = articles[1]
  const leftBottomArticle = articles[2]
  const rightTopArticle = articles[3]
  const rightBottomArticle = articles[4]

  return (
    <>
      <div className="my-container px-4 py-2">
        <h1 className="font-sans font-extrabold text-2xl xs:text-3xl underline decoration-2 underline-offset-4 my-12">
          Top #1
        </h1>

        <div className="flex flex-col sm:flex-row gap-1 md:gap-3">
          {/* column1 - parent */}
          <div className="2xl:flex flex-1 2xl:justify-end hidden sm:block">
            <div className="space-y-2">

              {/* column1 - children for first article */}
              <div className="flex-1">
                <Link
                  to={`article/${leftTopArticle.id}/detail`}
                  className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                  {/* title */}
                  <h1 className="font-serif text-2xl md:text-3xl font-extrabold mb-5 max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                    {language === "id" ? leftTopArticle.translated_title : leftTopArticle.title}
                  </h1>

                  {/* description */}
                  <p className="font-sans text-sm text-black font-light mb-5 max-w-77.5 leading-relaxed">
                    {language === "id" ? leftTopArticle.translated_description : leftTopArticle.description}
                  </p>

                  {/* author */}
                  <span className="font-sans text-xs md:text-sm font-medium mb-5 text-body-1st">
                    By {leftTopArticle.author}
                  </span>
                </Link>
              </div>

              <Separator className="bg-gray-300" />

              {/* column2 - children for second article */}
              <div className="flex-1 py-2">
                <Link
                  to={`article/${leftBottomArticle.id}/detail`}
                  className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                  {/* title */}
                  <h1 className="font-serif text-2xl md:text-3xl font-extrabold mb-5 max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                    {language === "id" ? leftBottomArticle.translated_title : leftBottomArticle.title}
                  </h1>

                  {/* author */}
                  <span className="font-sans text-xs md:text-sm font-medium mb-5 text-body-1st">
                    By {leftBottomArticle.author}
                  </span>
                </Link>
              </div>
            </div>
          </div>

          <Separator orientation="vertical" className="bg-gray-300" />

          {/* column2 - parent */}
          <div className="flex-1">
            <div className="flex flex-col justify-center">
              <Link
                to={`article/${mainArticle.id}/detail`}
                className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
              >
                {/* image */}
                <div className="mb-3 overflow-hidden shadow-md">
                  <img
                    src={mainArticle.image_url}
                    alt={mainArticle.title}
                    className="w-full h-auto bg-cover bg-center grayscale-90 transition-transform duration-500 ease-out md:group-hover:scale-[1.025]"
                  />
                </div>

                <h1 className="font-serif text-2xl md:text-3xl font-extrabold mb-5 sm:max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                  {language === "id" ? mainArticle.translated_title : mainArticle.title}
                </h1>

                {/* description */}
                <p className="font-sans text-sm text-black font-light mb-5 sm:max-w-77.5 leading-relaxed">
                  {language === "id" ? mainArticle.translated_description : mainArticle.description}
                </p>

                {/* author */}
                <span className="font-sans text-xs md:text-sm font-medium sm:mb-5 text-body-1st">
                  By {mainArticle.author}
                </span>
              </Link>
            </div>
          </div>

          <Separator orientation="vertical" className="bg-gray-300" />

          {/* column3 - parent */}
          <div className="flex-1 hidden sm:block">
            <div className="space-y-2">

              {/* column1 - children for first article */}
              <div className="flex-1">
                <Link
                  to={`article/${rightTopArticle.id}/detail`}
                  className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                  {/* image */}
                  <div className="mb-2 overflow-hidden shadow-md">
                    <img
                      src={rightTopArticle.image_url}
                      alt={rightTopArticle.title}
                      className="w-full h-50 bg-cover bg-center object-cover grayscale-90 transition-transform duration-500 ease-out md:group-hover:scale-[1.025]"
                    />
                  </div>

                  {/* title */}
                  <h1 className="font-serif text-xl md:text-2xl font-extrabold mb-3 max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                    {language === "id" ? rightTopArticle.translated_title : rightTopArticle.title}
                  </h1>

                  {/* author */}
                  <span className="font-sans text-xs md:text-sm font-medium mb-3 text-body-1st">
                    By {rightTopArticle.author}
                  </span>
                </Link>
              </div>

              {/* column2 - children for second article */}
              <div className="flex-1 mt-5">
                <Link
                  to={`article/${rightBottomArticle.id}/detail`}
                  className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                  {/* image */}
                  <div className="mb-2 overflow-hidden shadow-md">
                    <img
                      src={rightBottomArticle.image_url}
                      alt={rightBottomArticle.title}
                      className="w-full h-50 bg-cover bg-center object-cover grayscale-90 transition-transform duration-500 ease-out md:group-hover:scale-[1.025]"
                    />
                  </div>

                  {/* title */}
                  <h1 className="font-serif text-xl md:text-2xl font-extrabold mb-3 max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                    {language === "id" ? rightBottomArticle.translated_title : rightBottomArticle.title}
                  </h1>

                  {/* author */}
                  <span className="font-sans text-xs md:text-sm font-medium mb-5 text-body-1st">
                    By {rightBottomArticle.author}
                  </span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}