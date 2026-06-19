from src.handoff_generator import (
    HandoffGenerator
)

handoff = HandoffGenerator()

result = handoff.generate(

    persona="Frustrated User",

    issue="Password reset failure",

    conversation_history=[

        "User unable to login",

        "Password reset attempted"
    ],

    documents_used=[

        "password_reset_guide.pdf"
    ],

    attempted_steps=[

        "Forgot password",

        "Reset email checked"
    ],

    recommendation=

    "Investigate account lock status"
)

print(result)