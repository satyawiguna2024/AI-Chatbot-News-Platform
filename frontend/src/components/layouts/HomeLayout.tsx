import { Outlet } from "react-router"
import Navbar from "./Navbar"
import Footer from "./Footer"

export default function HomeLayout() {
  return (
    <>
      <div className="flex min-h-screen flex-col">
        <Navbar />

        <main className="my-container flex-1">
          <Outlet />
        </main>

        <Footer />
      </div>
    </>
  )
}
