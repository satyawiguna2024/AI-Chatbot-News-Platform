import { Outlet } from "react-router";
import { DialogChatbot } from "@/pages/chat-bot/DialogChatbot";
import { useArticles } from "@/hooks/queries/useArticles";
import Navbar from "./Navbar";
import Footer from "./Footer";
import PageLoading from "../shared/PageLoading";

export default function HomeLayout() {
  const { isLoading } = useArticles();
  if (isLoading) return <PageLoading />

  return (
    <>
      <div className="flex min-h-screen flex-col">
        <Navbar />

        <main className="my-container flex-1">
          <Outlet />
        </main>

        {/* modal asking with bot */}
        <DialogChatbot />

        <Footer />
      </div>
    </>
  );
}
