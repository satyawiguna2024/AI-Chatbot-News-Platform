import { Outlet } from "react-router";
import Footer from "./Footer";
import { DialogChatbot } from "@/pages/chat-bot/DialogChatbot";
import ButtonUp from "../costume-components/ButtonUp";

export default function ArticleDetailLayout() {
  return (
    <>
      <div>
        <main>
          <Outlet />
        </main>

        <DialogChatbot />
        <ButtonUp />

        <Footer />
      </div>
    </>
  )
}
