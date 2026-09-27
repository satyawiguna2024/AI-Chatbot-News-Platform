import {Routes, Route} from "react-router"
import HomeLayout from "./components/layouts/HomeLayout";
import ArticleDetailLayout from "./components/layouts/ArticleDetailLayout";
import MainArticle from "./pages/article/MainArticle";

export default function App() {
  return (
    <>
      <Routes>
        <Route element={<HomeLayout />}>
          <Route path="/" element={<MainArticle />} />
        </Route>

        <Route element={<ArticleDetailLayout />}>
          <Route path="/article/:id/detail" element={<h1>Detail Artikel</h1>} />
        </Route>
      </Routes>
    </>
  );
}