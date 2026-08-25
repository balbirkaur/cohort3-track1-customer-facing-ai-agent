from app.rag.knowledge_base import search_knowledge_base


results = search_knowledge_base(
    "My card payment failed but money was deducted"
)

for result in results:
    print("\n--- RESULT ---\n")
    print(result)