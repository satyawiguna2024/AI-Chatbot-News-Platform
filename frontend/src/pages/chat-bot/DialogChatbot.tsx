import {BotMessageSquare} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog"
import { ChatComponent } from "./Chat"

export function DialogChatbot() {
  return (
    <Dialog>
      <DialogTrigger
        render={
          <Button type="button" variant="outline" size="icon" aria-label="Ask with Bot" className="ai-pulse isolate fixed right-5 bottom-8 z-50 size-13 rounded-full border-title-1st/40 bg-beige-ringan text-title-1st shadow-[0_3px_10px_rgba(26,26,26,0.10),0_8px_24px_rgba(26,26,26,0.08)] transition-all duration-300 ease-out hover:scale-105 hover:border-title-1st/60 hover:bg-beige-ringan hover:shadow-[0_4px_12px_rgba(26,26,26,0.12),0_10px_28px_rgba(26,26,26,0.12)] active:scale-95 xl:size-14">
            <BotMessageSquare className="size-6 stroke-[1.8]" />
          </Button>
        }
      />

      <DialogContent
        showCloseButton={false}
        className="flex h-[min(560px,calc(100dvh-2rem))] w-[calc(100%-2rem)] max-w-sm flex-col gap-0 overflow-hidden rounded-3xl border-title-1st/15 bg-beige-ringan p-0"
      >
        <ChatComponent />
      </DialogContent>
    </Dialog>
  )
}