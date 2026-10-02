import { useState } from "react"
import { useParams } from "react-router"
import { ArrowUp, BotMessageSquare, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Message, MessageContent } from "@/components/ui/message"
import { Bubble, BubbleContent } from "@/components/ui/bubble"
import {
  MessageScroller,
  MessageScrollerButton,
  MessageScrollerContent,
  MessageScrollerItem,
  MessageScrollerProvider,
  MessageScrollerViewport,
} from "@/components/ui/message-scroller"
import { Textarea } from "@/components/ui/textarea"
import { useChatSession } from "@/hooks/useChatSession"
import { SourceCards } from "@/pages/chat-bot/SourceCards"

type ChatComponentProps = {
  open?: boolean
  onNavigate?: () => void // dipanggil saat user klik kartu sumber (untuk menutup modal)
}

export function ChatComponent({ open = true, onNavigate }: ChatComponentProps) {
  // route detail artikel: /article/:id/detail  -> sesuaikan nama param-nya
  const { id } = useParams()
  const articleId = id ? Number(id) : null

  const { messages, isReady, isStreaming, error, remaining, send } = useChatSession({
    open,
    articleId,
  })

  const [input, setInput] = useState("")

  const canSend = isReady && !isStreaming && input.trim().length > 0

  const handleSend = () => {
    if (!canSend) return
    send(input)
    setInput("")
  }

  return (
    <>
      <MessageScrollerProvider>
        {/* Header */}
        <div className="flex shrink-0 items-center justify-between border-b border-title-1st/10 px-5 py-4">
          <div>
            <h2 className="font-sans text-sm font-semibold text-title-1st">
              {articleId === null ? "Ask all articles" : "Ask this article"}
            </h2>

            <p className="mt-1 font-sans text-xs text-body-1st/60">
              {articleId === null
                ? "I'll search across all articles for you."
                : "I'll focus only on this article."}
            </p>
          </div>
        </div>

        {/* Messages */}
        <div className="min-h-0 flex-1 overflow-hidden">
          {!isReady && !error ? (
            <div className="flex h-full items-center justify-center">
              <Loader2 className="size-5 animate-spin text-body-1st/50" />
            </div>
          ) : messages.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center px-8 text-center">
              <div className="mb-4 flex size-10 items-center justify-center rounded-xl bg-title-1st/5">
                <BotMessageSquare className="size-5 text-title-1st" />
              </div>

              <h3 className="font-sans text-base font-semibold text-title-1st">
                Start a conversation
              </h3>

              <p className="mt-2 max-w-62.5 font-sans text-xs leading-5 text-body-1st/60">
                Ask me anything and I&apos;ll do my best to help you.
              </p>
            </div>
          ) : (
            <MessageScroller>
              <MessageScrollerViewport>
                <MessageScrollerContent className="gap-4 px-4 py-5">
                  {messages.map((message) => (
                    <MessageScrollerItem
                      key={message.id}
                      messageId={String(message.id)}
                      scrollAnchor={message.role === "user"}
                    >
                      <Message align={message.role === "user" ? "end" : "start"}>
                        <MessageContent>
                          <Bubble variant={message.role === "user" ? "default" : "outline"}>
                            <BubbleContent className="whitespace-pre-wrap text-sm leading-5">
                              {message.content || (
                                <span className="animate-pulse text-body-1st/50">
                                  Thinking...
                                </span>
                              )}
                            </BubbleContent>
                          </Bubble>

                          {/* Kartu sumber: hanya muncul kalau backend mengirim sources */}
                          {message.role === "assistant" && articleId === null && (
                            <SourceCards sources={message.sources} onNavigate={onNavigate} />
                          )}
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
          {error && (
            <p className="mb-2 rounded-lg bg-red-500/10 px-3 py-2 font-sans text-xs text-red-600">
              {error}
            </p>
          )}

          <form
            onSubmit={(event) => {
              event.preventDefault()
              handleSend()
            }}
            className="relative"
          >
            <Textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault()
                  handleSend()
                }
              }}
              disabled={!isReady}
              placeholder={isReady ? "Ask something..." : "Preparing chat..."}
              rows={2}
              className="min-h-24 resize-none rounded-2xl border-title-1st/10 bg-title-1st/5 pr-12 text-sm shadow-none focus-visible:border-title-1st/20 focus-visible:ring-title-1st/10"
            />

            <Button
              type="submit"
              size="icon"
              disabled={!canSend}
              aria-label="Send message"
              className="absolute right-2 bottom-2 size-8 rounded-full bg-title-1st text-beige-ringan hover:bg-title-1st/90 disabled:opacity-40"
            >
              {isStreaming ? (
                <Loader2 className="size-4 animate-spin" />
              ) : (
                <ArrowUp className="size-4" />
              )}
            </Button>
          </form>

          <p className="mt-2 text-center font-sans text-[10px] text-body-1st/50">
            AI can make mistakes. Check important information.
            {remaining !== null && ` · ${remaining} questions left`}
          </p>
        </div>
      </MessageScrollerProvider>
    </>
  )
}