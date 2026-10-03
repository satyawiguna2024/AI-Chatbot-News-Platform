export { cn } from "cn"

export function decodeHtml(text: string) {
  const el = document.createElement("textarea")
  el.innerHTML = text
  return el.value
}