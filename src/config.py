import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    CHROMA_DB_PATH = os.getenv(
        "CHROMA_DB_PATH",
        "chroma_db"
    )

    DB_PATH = os.getenv(
        "DB_PATH",
        "database/support_agent.db"
    )

    TOP_K = int(
        os.getenv("TOP_K", 5)
    )

    ESCALATION_THRESHOLD = float(
        os.getenv(
            "ESCALATION_THRESHOLD",
            0.55
        )
    )

    SUPPORTED_PERSONAS = [
        "Technical Expert",
        "Frustrated User",
        "Business Executive"
    ]

    SENSITIVE_KEYWORDS = [
        "billing",
        "refund",
        "payment",
        "legal",
        "lawsuit",
        "account locked",
        "security breach",
        "unauthorized access",
        "chargeback"
    ]