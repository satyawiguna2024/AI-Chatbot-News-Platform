import { Routes, Route } from "react-router"
import { LanguageProvider } from "./contexts/LanguageProvider";
import HomeLayout from "./components/layouts/HomeLayout";
import ArticleDetailLayout from "./components/layouts/ArticleDetailLayout";
import MainArticle from "./pages/article/MainArticle";
import DetailArticle from "./pages/detail-article/DetailArticle";

export default function App() {
  return (
    <>
      <LanguageProvider>
        <Routes>
          <Route element={<HomeLayout />}>
            <Route path="/" element={<MainArticle />} />
          </Route>

          <Route element={<ArticleDetailLayout />}>
            <Route path="/article/:id/detail" element={<DetailArticle />} />
          </Route>
        </Routes>
      </LanguageProvider>
    </>
  );
}