import re
from collections import Counter


class PersonaDetector:

    def __init__(self):

        self.technical_keywords = [
            "api",
            "authentication",
            "token",
            "jwt",
            "endpoint",
            "logs",
            "error",
            "exception",
            "stack trace",
            "configuration",
            "sdk",
            "integration",
            "latency",
            "request",
            "response",
            "debug",
            "database",
            "server",
            "ssl",
            "rate limit"
        ]

        self.frustrated_keywords = [
            "angry",
            "frustrated",
            "upset",
            "terrible",
            "bad",
            "hate",
            "not working",
            "broken",
            "still not working",
            "again",
            "worst",
            "immediately",
            "urgent",
            "asap",
            "nothing works",
            "ridiculous"
        ]

        self.business_keywords = [
            "business",
            "impact",
            "revenue",
            "customer",
            "operations",
            "downtime",
            "timeline",
            "executive",
            "stakeholder",
            "resolution",
            "risk",
            "priority",
            "performance",
            "service availability",
            "productivity"
        ]

    def _count_matches(
        self,
        text,
        keywords
    ):

        score = 0

        for keyword in keywords:

            if keyword.lower() in text.lower():
                score += 1

        return score

    def detect_persona(
        self,
        message
    ):

        technical_score = self._count_matches(
            message,
            self.technical_keywords
        )

        frustrated_score = self._count_matches(
            message,
            self.frustrated_keywords
        )

        business_score = self._count_matches(
            message,
            self.business_keywords
        )

        scores = {
            "Technical Expert": technical_score,
            "Frustrated User": frustrated_score,
            "Business Executive": business_score
        }

        highest_persona = max(
            scores,
            key=scores.get
        )

        highest_score = scores[highest_persona]

        if highest_score == 0:
            return {
                "persona": "Business Executive",
                "confidence": 0.50
            }

        total = sum(scores.values())

        confidence = round(
            highest_score / total,
            2
        )

        return {
            "persona": highest_persona,
            "confidence": confidence
        }