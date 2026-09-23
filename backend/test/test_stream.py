import asyncio
import time

from openai import AsyncOpenAI

from app.core import get_settings


async def main() -> None:
    settings = get_settings()

    async with AsyncOpenAI(
        base_url=settings.openrouter_base_url,
        api_key=settings.openrouter_api_key,
    ) as client:
        start = time.perf_counter()

        async with client.chat.completions.stream(
            model="nex-agi/nex-n2.5-pro:free",
            messages=[
                {
                    "role": "user",
                    "content": "Jelaskan apa itu PostgreSQL dalam 10 kalimat pendek.",
                }
            ],
            max_tokens=300,
        ) as stream:

            print("STREAM CREATED")

            async for event in stream:
                elapsed = time.perf_counter() - start

                if event.type == "content.delta":
                  print(
                    f"[{elapsed:.2f}s] {event.delta!r}",
                    flush=True,
                  )


if __name__ == "__main__":
    asyncio.run(main())