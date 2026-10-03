export function parseArticleId(param?: string): number | null {
  if (!param || !/^[1-9]\d*$/.test(param)) return null
  const id = Number(param)
  return Number.isSafeInteger(id) ? id : null
}