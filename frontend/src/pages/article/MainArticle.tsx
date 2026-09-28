import HeaderSection from "./HeaderSection";
import ListArticles from "./ListArticles";
import TrendingArticle from "./TrendingArticle";

export default function MainArticle() {
  return (
    <>
      {/* Top #1 Article */}
      <HeaderSection />

      {/* Latest Article */}
      <TrendingArticle />

      {/* Listing Article */}
      <ListArticles />
    </>
  )
}
