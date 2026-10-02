/* eslint-disable @typescript-eslint/no-explicit-any */
const ID_KEY = "askNews:anonymousId";
const SCOPE_KEY = "askNews:lastScope";

export function getAnonymousId(): string {
  try {
    let id = localStorage.getItem(ID_KEY);
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem(ID_KEY, id);
    }
    return id;
  } catch {
    // fallback kalau localStorage diblok (private mode, dll)
    return (window as any).__anonId ??= crypto.randomUUID();
  }
}

// scope = "root" atau id artikel (string)
export function getLastScope(): string | null {
  try {
    return localStorage.getItem(SCOPE_KEY);
  } catch {
    return null;
  }
}

export function setLastScope(scope: string) {
  try {
    localStorage.setItem(SCOPE_KEY, scope);
  } catch {
    /* ignore */
  }
}