import { useState } from "react"
import { ArrowUp, BotMessageSquare, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog"
import { Message, MessageContent } from "@/components/ui/message"
import { Bubble, BubbleContent } from "@/components/ui/bubble"
import { MessageScroller, MessageScrollerButton, MessageScrollerContent, MessageScrollerItem, MessageScrollerProvider, MessageScrollerViewport } from "@/components/ui/message-scroller"
import { Textarea } from "@/components/ui/textarea"

type ChatMessage = {
  id: string
  role: "user" | "assistant"
  content: string
}

type DialogChatbotProps = {
  article?: {
    id: number
    title: string
  }
}

export function DialogChatbot({ article }: DialogChatbotProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")

  const handleSend = () => {
    const content = input.trim()

    if (!content) {
      return
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content,
    }

    setMessages((current) => [...current, userMessage])
    setInput("")
  }

  return (
    <Dialog>
      <DialogTrigger
        render={
          <Button type="button" variant="outline" size="icon" aria-label="Ask with Bot" className="ai-pulse isolate fixed right-5 bottom-8 z-50 size-13 rounded-full border-title-1st/40 bg-beige-ringan text-title-1st shadow-[0_3px_10px_rgba(26,26,26,0.10),0_8px_24px_rgba(26,26,26,0.08)] transition-all duration-300 ease-out hover:scale-105 hover:border-title-1st/60 hover:bg-beige-ringan hover:shadow-[0_4px_12px_rgba(26,26,26,0.12),0_10px_28px_rgba(26,26,26,0.12)] active:scale-95 xl:size-14">
            <BotMessageSquare className="size-6 stroke-[1.8]" />
          </Button>
        }
      />

      <DialogContent showCloseButton={false} className="flex h-[min(560px,calc(100dvh-2rem))] w-[calc(100%-2rem)] max-w-sm flex-col gap-0 overflow-hidden rounded-3xl border-title-1st/15 bg-beige-ringan p-0">
        <MessageScrollerProvider>
          {/* Header */}
          <div className="flex shrink-0 items-center justify-between border-b border-title-1st/10 px-5 py-4">
            <div>
              <h2 className="font-sans text-sm font-semibold text-title-1st">
                {article ? "Ask about this article" : "New Chat"}
              </h2>

              <p className="mt-1 font-sans text-xs text-body-1st/60">
                {article ? "I can help you understand this article." : "How can I help you today?"}
              </p>
            </div>
          </div>

          {/* Messages */}
          <div className="min-h-0 flex-1 overflow-hidden">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center px-8 text-center">
                <div className="mb-4 flex size-10 items-center justify-center rounded-xl bg-title-1st/5">
                  <BotMessageSquare className="size-5 text-title-1st" />
                </div>

                <h3 className="font-sans text-base font-semibold text-title-1st">
                  {article ? "Ask about this article" : "Start a conversation"}
                </h3>

                <p className="mt-2 max-w-62.5 font-sans text-xs leading-5 text-body-1st/60">
                  {article
                    ? "Ask anything about this article and I&apos;ll help you understand the information."
                    : "Ask me anything and I&apos;ll do my best to help you."}
                </p>
              </div>
            ) : (
              <MessageScroller>
                <MessageScrollerViewport>
                  <MessageScrollerContent className="gap-4 px-4 py-5">
                    {messages.map((message) => (
                      <MessageScrollerItem key={message.id} messageId={message.id} scrollAnchor={message.role === "user"}>
                        <Message align={message.role === "user" ? "end" : "start"}>
                          <MessageContent>
                            <Bubble variant={message.role === "user" ? "default" : "outline"}>
                              <BubbleContent className="text-sm leading-5">
                                {message.content}
                              </BubbleContent>
                            </Bubble>
                          </MessageContent>
                        </Message>
                      </MessageScrollerItem>
                    ))}
                  </MessageScrollerContent>
                </MessageScrollerViewport>

                <MessageScrollerButton />
              </MessageScroller>
            )}
          </div>

          {/* Input */}
          <div className="shrink-0 border-t border-title-1st/10 p-4">
            {article && (
              <div className="mb-3 flex items-center gap-2 rounded-xl border border-title-1st/10 bg-title-1st/5 px-3 py-2">
                <FileText className="size-4 shrink-0 text-title-1st/60" />

                <div className="min-w-0">
                  <p className="font-sans text-[10px] font-medium uppercase tracking-wide text-body-1st/50">
                    About this article
                  </p>

                  <p className="mt-0.5 truncate font-sans text-xs font-medium text-title-1st">
                    {article.title}
                  </p>
                </div>
              </div>
            )}

            <form onSubmit={(event) => { event.preventDefault(); handleSend() }} className="relative">
              <Textarea
                value={input}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault()
                    handleSend()
                  }
                }}
                placeholder={article ? "Ask about this article..." : "Ask something..."}
                rows={2}
                className="min-h-24 resize-none rounded-2xl border-title-1st/10 bg-title-1st/5 pr-12 text-sm shadow-none focus-visible:border-title-1st/20 focus-visible:ring-title-1st/10"
              />

              <Button type="submit" size="icon" disabled={!input.trim()} aria-label="Send message" className="absolute right-2 bottom-2 size-8 rounded-full bg-title-1st text-beige-ringan hover:bg-title-1st/90 disabled:opacity-40">
                <ArrowUp className="size-4" />
              </Button>
            </form>

            <p className="mt-2 text-center font-sans text-[10px] text-body-1st/50">
              AI can make mistakes. Check important information.
            </p>
          </div>
        </MessageScrollerProvider>
      </DialogContent>
    </Dialog>
  )
}