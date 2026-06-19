from src.rag_pipeline import RAGPipeline

rag = RAGPipeline()

results = rag.retrieve(
    "How do I reset my password?"
)

for item in results:

    print("\n")

    print(
        "SOURCE:",
        item["source"]
    )

    print(
        "PAGE:",
        item["page"]
    )

    print(
        "CONFIDENCE:",
        item["confidence"]
    )

    print(
        item["content"][:200]
    )