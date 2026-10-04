import { Routes, Route } from "react-router"
import { LanguageProvider } from "./contexts/LanguageProvider";
import HomeLayout from "./components/layouts/HomeLayout";
import ArticleDetailLayout from "./components/layouts/ArticleDetailLayout";
import MainArticle from "./pages/article/MainArticle";
import DetailArticle from "./pages/detail-article/DetailArticle";
import NotFound from "./components/shared/NotFound";

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

          {/* page not found */}
          <Route path="*" element={<NotFound title="Not Found Pages" description="The page you are looking for does not exist." />} />
        </Routes>
      </LanguageProvider>
    </>
  );
}