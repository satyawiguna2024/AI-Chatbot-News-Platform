import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

export function MarkdownMessage({ content }: { content: string }) {
  return (
    <div className="whitespace-normal wrap-break-word [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children }) => <p className="my-2 leading-6">{children}</p>,
          strong: ({ children }) => (
            <strong className="font-semibold text-title-1st">{children}</strong>
          ),
          ul: ({ children }) => (
            <ul className="my-2 list-disc space-y-1.5 pl-5 marker:text-title-1st/50">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="my-2 list-decimal space-y-1.5 pl-5 marker:text-title-1st/50">{children}</ol>
          ),
          li: ({ children }) => (
            <li className="pl-1 leading-6 [&>p]:my-0 [&>p]:inline">{children}</li>
          ),
          h1: ({ children }) => <h3 className="mt-3 mb-1 text-base font-semibold">{children}</h3>,
          h2: ({ children }) => <h3 className="mt-3 mb-1 text-base font-semibold">{children}</h3>,
          h3: ({ children }) => <h3 className="mt-3 mb-1 text-sm font-semibold">{children}</h3>,
          a: ({ children, href }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="underline underline-offset-2"
            >
              {children}
            </a>
          ),
          code: ({ children }) => (
            <code className="rounded bg-title-1st/10 px-1 py-0.5 text-xs">{children}</code>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}