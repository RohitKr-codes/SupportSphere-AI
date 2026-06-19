from src.persona_detector import PersonaDetector

detector = PersonaDetector()

queries = [

    "Can you provide the API logs and authentication error details?",

    "Nothing works. I am extremely frustrated and need help now!",

    "What is the business impact and estimated resolution timeline?"
]

for query in queries:

    result = detector.detect_persona(
        query
    )

    print(
        query,
        "\n",
        result,
        "\n"
    )