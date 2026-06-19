class SentimentAnalyzer:

    def __init__(self):

        self.negative_words = [
            "angry",
            "upset",
            "hate",
            "bad",
            "terrible",
            "urgent",
            "worst",
            "broken",
            "frustrated",
            "issue",
            "problem",
            "failed"
        ]

        self.positive_words = [
            "great",
            "good",
            "thanks",
            "awesome",
            "perfect",
            "resolved",
            "helpful"
        ]

    def analyze(
        self,
        text
    ):

        text = text.lower()

        negative_score = sum(
            word in text
            for word in self.negative_words
        )

        positive_score = sum(
            word in text
            for word in self.positive_words
        )

        if negative_score > positive_score:
            return "Negative"

        if positive_score > negative_score:
            return "Positive"

        return "Neutral"