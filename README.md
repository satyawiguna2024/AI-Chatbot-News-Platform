
Membersihkan seluruh folder pycache
```
find . -type d -name "__pycache__" -exec rm -rf {} +

find . -name "*--py"

find . -name "*--py" -delete
```

Todo `/backend`:
```
-- ✅ Project setup
-- ✅ PostgreSQL connection
-- ✅ Database schema / model
-- ✅ Database migration dengan Alembic
-- ✅ NewsAPI integration
-- ✅ Translate English -> Indonesia
-- ✅ Menyimpan berita ke PostgreSQL
-- ✅ Chunking artikel
-- ✅ Menyimpan Chunking kedalam Database Postgres
-- ✅ Embedding dengan OpenAI
-- ✅ pgvector + similarity search
-- ✅ RAG
-- ✅ Chat endpoint
-- ✅ Token Optimization
-- ✅ Conversation
      -- ✅ Chat route bisa mendapatkan/membuat conversation
      -- ✅ RAG menerima conversation_id
-- ✅ Message
      -- ✅ Ambil recent messages
      -- ✅ Simpan user/assistant message
-- ✅ conversation memory
-- ✅ anonymous guest lifecycle
-- Rate limiting / validation / logging
-- ✅ Testing & production hardening
```

Todo `/frontend`:
```
```


Mengatasi tamu tamu datang untuk conversation:
```
                    Guest
                      |
                      |
                 Conversation
                      │
             ┌────────┴────────┐
             │                 │
       pindah context      tidak aktif
             │                 │
             ↓                 ↓
          DELETE          TTL expired


Jadi kita sekarang punya aturan yang sangat jelas:

1 guest → 1 active conversation → 1 current path/context.

Close popup dan refresh → keep.
Pindah path → delete.
Guest hilang tanpa bisa dideteksi → TTL sebagai fallback.


---------------------------------------

Mengatasi Hemat token untuk message:

ambil pesan terbaru
↓
hitung token
↓
berhenti ketika mencapai ~800 token

---------------------------------------

contoh, hanya mengambil dari belakang atau bisa dibilang yang terbaru:

message 5 → 150
message 4 → 200
message 3 → 180
message 2 → 250
-----------------
780 tokens

---------------------------------------

finnal arsitektur hemat token message user:

                         USER QUESTION
                              │
                              ▼
                        Embed question
                              │
                              ▼
                        pgvector search
                              │
                    ┌─────────┴─────────┐
                    │                   │
             article_id exists      global chat
                    │                   │
                    ▼                   ▼
             article filter       global retrieval
                    │
                    ▼
             similarity threshold
                    │
                    ▼
                TOP 3 chunks
                    │
                    ▼
          ┌─────────────────────┐
          │ Build small context │
          └─────────────────────┘
                    │
                    │
          Recent conversation
          max ~500–800 tokens
                    │
                    ▼
              Chat Completion
                    │
             output ≤ ~300
                    │
                    ▼
                  ANSWER

```


```
curl -N -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "anonymous_id": "220ccd2a-536f-40f5-8f48-a436a174749b",
    "article_id": 1,
    "question": "Apa yang dibahas dalam artikel ini?"
  }'
```