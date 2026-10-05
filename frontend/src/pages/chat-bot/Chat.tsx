import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router";
import {
  MessageScroller,
  MessageScrollerButton,
  MessageScrollerContent,
  MessageScrollerItem,
  MessageScrollerProvider,
  MessageScrollerViewport,
} from "@/components/ui/message-scroller";
import { Button } from "@/components/ui/button";
import { Message, MessageContent } from "@/components/ui/message";
import { Bubble, BubbleContent } from "@/components/ui/bubble";
import { Textarea } from "@/components/ui/textarea";
import { MarkdownMessage } from "@/components/shared/MarkdownMessage";
import { ThinkingStatus } from "@/components/shared/ThinkingStatus";
import { parseArticleId } from "@/lib/articleId";
import { decodeHtml } from "@/lib/utils";
import { useChatSession } from "@/hooks/useChatSession";
import { useArticle } from "@/hooks/queries/useArticle";
import { SourceCards } from "@/pages/chat-bot/SourceCards";
import type { ChatComponentProps } from "@/types/chat";
import IconAskNews from "@/assets/icons/icon-asknews.png";
import { ArrowUp, BotMessageSquare, FileText, Loader2 } from "lucide-react";

const PUBLIC_QUICK_CHATS = [
  "What are the most popular news articles this year?",
  "What are the latest trending news in Indonesia?",
];

const ARTICLE_QUICK_CHATS = [
  "What is this article about?",
  "Can you summarize this article?",
];

export function ChatComponent({ open = true, onNavigate }: ChatComponentProps) {
  const { id: idParam } = useParams();
  const id = parseArticleId(idParam);
  const articleId = id ? Number(id) : null;

  const { messages, isReady, isStreaming, error, remaining, send } =
    useChatSession({
      open,
      articleId,
    });

  const { data: currentArticle } = useArticle(articleId ?? 0);

  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  const quickChats =
    articleId !== null ? ARTICLE_QUICK_CHATS : PUBLIC_QUICK_CHATS;

  const canSend = isReady && !isStreaming && input.trim().length > 0;

  const handleSend = () => {
    if (!canSend) return;

    send(input);
    setInput("");
  };

  const handleQuickChat = (question: string) => {
    if (!isReady || isStreaming) return;

    send(question);
  };

  useEffect(() => {
    const el = bottomRef.current;

    if (!el) return;

    let parent = el.parentElement;

    while (parent && parent.scrollHeight <= parent.clientHeight) {
      parent = parent.parentElement;
    }

    parent?.scrollTo({
      top: parent.scrollHeight,
    });
  }, [messages]);

  return (
    <>
      <MessageScrollerProvider>
        {/* Header */}
        <div className="flex shrink-0 items-center justify-between border-b border-title-1st/10 px-5 py-4">
          <div>
            <span className="flex items-center">
              <img src={IconAskNews} alt="Icon AskNews" className="size-10" />

              <h3 className="font-sans text-sm font-semibold text-title-1st">
                Ask News
              </h3>
            </span>
          </div>
        </div>

        {/* Messages */}
        <div className="min-h-0 flex-1 overflow-hidden">
          {!isReady && !error ? (
            <div className="flex h-full items-center justify-center">
              <Loader2 className="size-5 animate-spin text-body-1st/50" />
            </div>
          ) : messages.length === 0 ? (
            <div className="flex h-full flex-col justify-center px-6">
              {/* Welcome icon */}
              <div className="mb-4 flex size-10 items-center justify-center rounded-xl bg-title-1st/5">
                <BotMessageSquare className="size-5 text-title-1st" />
              </div>

              {/* Welcome title */}
              <h3 className="font-sans text-base font-semibold text-title-1st">
                {articleId !== null
                  ? "Ask about this article"
                  : "What would you like to know?"}
              </h3>

              {/* Welcome description */}
              <p className="mt-2 max-w-72 font-sans text-xs leading-5 text-body-1st/60">
                {articleId !== null
                  ? "Choose a question below to explore this article."
                  : "Choose a question below to explore Indonesian news."}
              </p>

              {/* Quick chats */}
              <div className="mt-5 flex flex-col gap-2">
                {quickChats.map((question) => (
                  <button
                    key={question}
                    type="button"
                    onClick={() => handleQuickChat(question)}
                    disabled={!isReady || isStreaming}
                    className="rounded-xl border border-title-1st/10 bg-title-1st/5 px-3 py-2.5 text-left font-sans text-xs leading-5 text-title-1st transition hover:border-title-1st/20 hover:bg-title-1st/10 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <MessageScroller>
              <MessageScrollerViewport>
                <MessageScrollerContent className="gap-4 px-4 py-5">
                  {messages.map((message) => (
                    <MessageScrollerItem
                      key={message.id}
                      messageId={String(message.id)}
                    >
                      <Message
                        align={message.role === "user" ? "end" : "start"}
                      >
                        <MessageContent>
                          <Bubble
                            variant={
                              message.role === "user" ? "default" : "outline"
                            }
                          >
                            <BubbleContent className="text-sm leading-5">
                              {message.content ? (
                                message.role === "assistant" ? (
                                  <MarkdownMessage content={message.content} />
                                ) : (
                                  <span className="whitespace-pre-wrap">
                                    {message.content}
                                  </span>
                                )
                              ) : (
                                <ThinkingStatus
                                  isArticle={articleId !== null}
                                />
                              )}
                            </BubbleContent>
                          </Bubble>

                          {/* Sources hanya ditampilkan jika backend mengirim sources */}
                          {message.role === "assistant" &&
                            articleId === null && (
                              <SourceCards
                                sources={message.sources}
                                onNavigate={onNavigate}
                              />
                            )}
                        </MessageContent>
                      </Message>
                    </MessageScrollerItem>
                  ))}

                  <div ref={bottomRef} />
                </MessageScrollerContent>
              </MessageScrollerViewport>

              <MessageScrollerButton />
            </MessageScroller>
          )}
        </div>

        {/* Input */}
        <div className="shrink-0 border-t border-title-1st/10 p-4">
          {/* Currently reading */}
          {articleId !== null && currentArticle && (
            <div className="mb-3 flex items-start gap-2 rounded-xl border border-title-1st/10 bg-title-1st/5 px-3 py-2">
              <FileText className="mt-0.5 size-3.5 shrink-0 text-body-1st/60" />

              <div className="min-w-0">
                <p className="font-sans text-[10px] uppercase tracking-wider text-body-1st/60">
                  Currently reading
                </p>

                <p className="line-clamp-2 font-sans text-xs font-medium text-title-1st">
                  {decodeHtml(currentArticle.title)}
                </p>
              </div>
            </div>
          )}

          {/* Error */}
          {error && (
            <p className="mb-2 rounded-lg bg-red-500/10 px-3 py-2 font-sans text-xs text-red-600">
              {error}
            </p>
          )}

          {/* Input */}
          <form
            onSubmit={(event) => {
              event.preventDefault();
              handleSend();
            }}
            className="relative"
          >
            <Textarea
              value={input}
              onChange={(event) => {
                setInput(event.target.value);
              }}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  handleSend();
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

          {/* Disclaimer + quota */}
          <p className="mt-2 text-center font-sans text-[10px] text-body-1st/50">
            AI can make mistakes. Check important information.
            {remaining !== null && ` · ${remaining} questions left`}
          </p>
        </div>
      </MessageScrollerProvider>
    </>
  );
}
