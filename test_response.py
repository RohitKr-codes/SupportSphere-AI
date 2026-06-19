from src.persona_detector import PersonaDetector
from src.rag_pipeline import RAGPipeline
from src.response_generator import ResponseGenerator


query = """
I forgot my password and
cannot login.
"""

detector = PersonaDetector()

persona_result = detector.detect_persona(
    query
)

persona = persona_result["persona"]

rag = RAGPipeline()

docs = rag.retrieve(query)

generator = ResponseGenerator()

response = generator.generate_response(
    query,
    persona,
    docs
)

print("\nPERSONA:")
print(persona)

print("\nRESPONSE:\n")
print(response)