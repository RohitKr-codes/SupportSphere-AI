from src.rag_pipeline import RAGPipeline
from src.escalation_manager import (
    EscalationManager
)

query = """
My billing dispute needs
legal review immediately.
"""

rag = RAGPipeline()

docs = rag.retrieve(query)

manager = EscalationManager()

status, reason = (
    manager.should_escalate(
        query,
        docs
    )
)

print(status)
print(reason)