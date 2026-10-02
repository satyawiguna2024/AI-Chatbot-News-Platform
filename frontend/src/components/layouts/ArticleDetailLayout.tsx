import { Outlet } from "react-router";
import Footer from "./Footer";
import { DialogChatbot } from "@/pages/chat-bot/DialogChatbot";

export default function ArticleDetailLayout() {
  return (
    <>
      <div>
        <main>
          <Outlet />
        </main>

        <DialogChatbot />
        
        <Footer />
      </div>
    </>
  )
}
