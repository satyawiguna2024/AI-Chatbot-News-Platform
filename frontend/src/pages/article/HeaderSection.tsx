import { Separator } from "@/components/ui/separator"
import { Link } from "react-router"

export default function HeaderSection() {
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
                  to="/"
                  className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                  {/* title */}
                  <h1 className="font-serif text-2xl md:text-3xl font-extrabold mb-5 max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ratione, maxime?
                  </h1>

                  {/* description */}
                  <p className="font-sans text-sm text-black font-light mb-5 max-w-77.5 leading-relaxed">
                    Lorem, ipsum dolor sit amet consectetur adipisicing elit. Sint ipsum vitae molestias error maxime, repudiandae possimus quaerat voluptatum illum unde!
                  </p>

                  {/* author */}
                  <span className="font-sans text-xs md:text-sm font-medium mb-5 text-body-1st">
                    By Isya Rahaladia
                  </span>
                </Link>
              </div>

              <Separator className="bg-gray-300" />

              {/* column2 - children for second article */}
              <div className="flex-1 py-2">
                <Link
                  to="/"
                  className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                  {/* title */}
                  <h1 className="font-serif text-2xl md:text-3xl font-extrabold mb-5 max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ratione, maxime?
                  </h1>

                  {/* author */}
                  <span className="font-sans text-xs md:text-sm font-medium mb-5 text-body-1st">
                    By Pralabo
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
                to="/"
                className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
              >
                {/* image */}
                <div className="mb-3 overflow-hidden shadow-md">
                  <img
                    src="https://images.unsplash.com/photo-1790108931626-f26b56184fb8?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                    alt="Unplash"
                    className="w-full h-auto bg-cover bg-center grayscale-90 transition-transform duration-500 ease-out md:group-hover:scale-[1.025]"
                  />
                </div>

                <h1 className="font-serif text-2xl md:text-3xl font-extrabold mb-5 sm:max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                  Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ratione, maxime?
                </h1>

                {/* description */}
                <p className="font-sans text-sm text-black font-light mb-5 sm:max-w-77.5 leading-relaxed">
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt totam illum, at repellendus saepe laboriosam natus ipsam sequi facilis dolore corrupti cupiditate molestias? Amet animi hic debitis eveniet autem. Pariatur.
                </p>

                {/* author */}
                <span className="font-sans text-xs md:text-sm font-medium sm:mb-5 text-body-1st">
                  By Hils
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
                  to="/"
                  className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                  {/* image */}
                  <div className="mb-2 overflow-hidden shadow-md">
                    <img
                      src="https://images.unsplash.com/photo-1789313946184-f5e04a0fc410?q=80&w=774&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                      alt="Unplash"
                      className="w-full h-50 bg-cover bg-center object-cover grayscale-90 transition-transform duration-500 ease-out md:group-hover:scale-[1.025]"
                    />
                  </div>

                  {/* title */}
                  <h1 className="font-serif text-xl md:text-2xl font-extrabold mb-3 max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ratione, maxime?
                  </h1>

                  {/* author */}
                  <span className="font-sans text-xs md:text-sm font-medium mb-3 text-body-1st">
                    By Ahmads
                  </span>
                </Link>
              </div>

              {/* column2 - children for second article */}
              <div className="flex-1 mt-5">
                <Link
                  to="/"
                  className="group cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-4"
                >
                  {/* image */}
                  <div className="mb-2 overflow-hidden shadow-md">
                    <img
                      src="https://images.unsplash.com/photo-1790137751714-476f99f978bf?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                      alt="Unplash"
                      className="w-full h-50 bg-cover bg-center object-cover grayscale-90 transition-transform duration-500 ease-out md:group-hover:scale-[1.025]"
                    />
                  </div>

                  {/* title */}
                  <h1 className="font-serif text-xl md:text-2xl font-extrabold mb-3 max-w-85 leading-7 md:group-hover:underline md:group-hover:decoration-1 md:group-hover:underline-offset-4">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ratione, maxime?
                  </h1>

                  {/* author */}
                  <span className="font-sans text-xs md:text-sm font-medium mb-5 text-body-1st">
                    By James
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