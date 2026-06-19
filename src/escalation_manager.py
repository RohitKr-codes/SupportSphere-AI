from src.config import Config


class EscalationManager:

    def should_escalate(
        self,
        query,
        retrieved_docs
    ):

        query_lower = query.lower()

        for keyword in Config.SENSITIVE_KEYWORDS:

            if keyword in query_lower:

                return True, (
                    "Sensitive issue detected"
                )

        if not retrieved_docs:

            return True, (
                "No documents found"
            )

        highest_confidence = max(
            [
                doc["confidence"]
                for doc in retrieved_docs
            ],
            default=0
        )

        if (
            highest_confidence
            < Config.ESCALATION_THRESHOLD
        ):

            return True, (
                "Low retrieval confidence"
            )

        return False, (
            "No escalation needed"
        )