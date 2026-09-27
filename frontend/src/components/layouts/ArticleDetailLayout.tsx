import { Outlet } from "react-router";
import Footer from "./Footer";

export default function ArticleDetailLayout() {
  return (
    <>
      <div>
        <main>
          <Outlet />
        </main>

        <Footer />
      </div>
    </>
  )
}
