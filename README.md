
Membersihkan seluruh folder pycache
```
find . -type d -name "__pycache__" -exec rm -rf {} +
```

Todo ```/backend``` directory:
```
1. ✅ Project setup
2. ✅ PostgreSQL connection
3. ➡️ Database schema / model
4. Database migration dengan Alembic
5. NewsAPI integration
6. Menyimpan berita ke PostgreSQL
7. Deduplication
8. Chunking artikel
9. Embedding dengan OpenAI
10. pgvector + similarity search
11. RAG
12. Chat endpoint
13. Rate limiting / validation / logging
14. Testing & production hardening
```