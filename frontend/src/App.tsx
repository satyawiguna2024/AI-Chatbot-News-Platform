import {Routes, Route} from "react-router"
import HomeLayout from "./components/layouts/HomeLayout";
import ArticleDetailLayout from "./components/layouts/ArticleDetailLayout";

export default function App() {
  return (
    <>
      <Routes>
        <Route element={<HomeLayout />}>
          <Route path="/" element={<h1>Home</h1>} />
        </Route>

        <Route element={<ArticleDetailLayout />}>
          <Route path="/article/:id/detail" element={<h1>Detail Artikel</h1>} />
        </Route>
      </Routes>
    </>
  );
}