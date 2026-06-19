from src.analytics import Analytics
from src.feedback_manager import (
    FeedbackManager
)

analytics = Analytics()

analytics.log_query(

    "Technical Expert",

    "API authentication issue",

    False
)

feedback = FeedbackManager()

feedback.save_feedback(

    5,

    "Excellent response"
)

print("Database OK")