import pytest

from app.services import RAGChatService


@pytest.mark.asyncio
async def test_rag_chat():
  rag_chat = RAGChatService()

  question = "Berapa target jumlah desa nelayan yang akan dibangun pemerintah?"
  context = """
  The government has fast-tracked priority programs,
  including the construction of 5,000 fishing villages
  by the end of 2029.

  The Ministry of Marine Affairs and Fisheries previously
  constructed 100 KNMPs in 2025 and plans to develop
  1,269 locations in 2026.
  """

  answer = await rag_chat.generate_answer(question=question, context=context)

  print("\n=== RAG ANSWER ===")
  print(answer)

  assert answer