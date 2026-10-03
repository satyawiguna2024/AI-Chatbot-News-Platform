import { Outlet, useParams } from "react-router";
import { DialogChatbot } from "@/pages/chat-bot/DialogChatbot";
import { parseArticleId } from "@/lib/articleId";
import { useArticle } from "@/hooks/queries/useArticle";
import Footer from "./Footer";
import ButtonUp from "../shared/ButtonUp";

export default function ArticleDetailLayout() {
  const { id: idParam } = useParams()
  const id = parseArticleId(idParam)
  const { data: article, isLoading } = useArticle(id ?? 0)
  const showExtras = id !== null && !isLoading && Boolean(article)


  return (
    <>
      <div>
        <main>
          <Outlet />
        </main>

        {showExtras && (
          <>
            <Footer />
            <ButtonUp />
            <DialogChatbot />
          </>
        )}
      </div>
    </>
  )
}
