import re


class ArticleContentCleaner:
  BOILERPLATE_PATTERNS = [
    r"^Related news:",
    r"^Translator:",
    r"^Editor:",
    r"^Copyright ©",
  ]

  def clean(self, content: str):
    if not content:
      return ""

    content = content.strip()
    lines = content.splitlines()
    cleaned_lines: list[str] = []

    for line in lines:
      line = line.strip()

      if not line:
        continue

      if self._is_boilerplate(line):
        break

      cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()

  def _is_boilerplate(self, line: str):
    return any(
      re.match(pattern, line, flags=re.IGNORECASE)
      for pattern in self.BOILERPLATE_PATTERNS
    )