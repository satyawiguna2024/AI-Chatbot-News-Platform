import { Link } from "react-router";

export default function ListArticles() {
  return (
    <>
      <div className="my-container px-4 py-2">
        <h1 className="mt-16 mb-20 font-sans text-2xl font-extrabold underline decoration-2 underline-offset-4 xs:text-3xl sm:mt-36">
          Articles
        </h1>

        <div className="grid grid-cols-2 gap-5 xs:grid-cols-3 md:grid-cols-4">
          {Array.from({ length: 16 }).map((_, i) => (
            <div
              key={i}
              className="relative flex flex-col justify-center border-gray-300 pr-0 sm:pr-5"
            >
              <Link
                to="/"
                className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                <div className="mb-3 overflow-hidden shadow-md">
                  <img
                    src="https://images.unsplash.com/photo-1790108931626-f26b56184fb8?q=80&w=1740&auto=format&fit=crop"
                    alt="Unsplash"
                    className="h-auto w-full grayscale-90 transition-[transform,filter,box-shadow] duration-500 ease-out group-hover:scale-[1.025] group-hover:shadow-lg"
                  />
                </div>

                {/* author - publishAt */}
                <span className="mb-4 flex justify-between">
                  <span className="font-sans text-[11px] font-medium text-body-1st">
                    By DR...
                  </span>

                  <span className="font-sans text-[11px] font-medium text-body-1st">
                    17-08-1945
                  </span>
                </span>

                {/* Title */}
                <h1 className="mb-3 font-serif text-[15px] font-extrabold leading-4 transition-[text-decoration] duration-300 md:text-lg md:leading-5 group-hover:underline group-hover:decoration-1 group-hover:underline-offset-4">
                  Lorem ipsum dolor sit amet consectetu...
                </h1>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}