import streamlit as st
import uuid

from src.persona_detector import PersonaDetector
from src.rag_pipeline import RAGPipeline
from src.response_generator import ResponseGenerator
from src.escalation_manager import EscalationManager
from src.handoff_generator import HandoffGenerator
from src.conversation_memory import ConversationMemory
from src.database import DatabaseManager
from src.analytics import Analytics
from src.feedback_manager import FeedbackManager


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Adsparkx AI Support Agent",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# ==========================================
# LOAD COMPONENTS
# ==========================================

@st.cache_resource
def load_components():

    return (
        PersonaDetector(),
        RAGPipeline(),
        ResponseGenerator(),
        EscalationManager(),
        HandoffGenerator(),
        ConversationMemory(),
        DatabaseManager(),
        Analytics(),
        FeedbackManager()
    )


(
    detector,
    rag,
    generator,
    escalation,
    handoff,
    memory,
    database,
    analytics,
    feedback_manager
) = load_components()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🤖 Adsparkx AI")

    st.markdown("---")

    st.subheader("Assignment Features")

    st.success("Persona Detection")
    st.success("RAG Knowledge Retrieval")
    st.success("Adaptive Response Generation")
    st.success("Human Escalation")
    st.success("Human Handoff Summary")
    st.success("Conversation Memory")
    st.success("SQLite Database")
    st.success("Analytics Logging")
    st.success("Feedback Collection")

    st.markdown("---")

    st.info(
        "AI Engineering Internship Assignment"
    )

    st.markdown("---")

    st.caption(
        f"Session ID:\n{st.session_state.session_id[:8]}"
    )


# ==========================================
# HEADER
# ==========================================

st.title(
    "🤖 Persona-Aware Customer Support Agent"
)

st.caption(
    "LLM + RAG + Human Escalation Workflow"
)


# ==========================================
# DISPLAY PREVIOUS CHAT
# ==========================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(
            msg["content"]
        )


# ==========================================
# USER INPUT
# ==========================================

user_query = st.chat_input(
    "Ask a support question..."
)


# ==========================================
# MAIN WORKFLOW
# ==========================================

if user_query:

    memory.add_message(
        st.session_state.session_id,
        "user",
        user_query
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("user"):

        st.markdown(
            user_query
        )

    # ----------------------------------
    # PERSONA DETECTION
    # ----------------------------------

    persona_result = (
        detector.detect_persona(
            user_query
        )
    )

    persona = (
        persona_result["persona"]
    )

    confidence = (
        persona_result["confidence"]
    )

    # ----------------------------------
    # RAG RETRIEVAL
    # ----------------------------------

    docs = rag.retrieve(
        user_query
    )

    # ----------------------------------
    # ESCALATION CHECK
    # ----------------------------------

    escalate, reason = (
        escalation.should_escalate(
            user_query,
            docs
        )
    )

    # ----------------------------------
    # RESPONSE GENERATION
    # ----------------------------------

    response = (
        generator.generate_response(
            user_query,
            persona,
            docs
        )
    )

    memory.add_message(
        st.session_state.session_id,
        "assistant",
        response
    )

    # ----------------------------------
    # DATABASE LOGGING
    # ----------------------------------

    database.save_conversation(
        st.session_state.session_id,
        persona,
        user_query,
        response,
        confidence,
        int(escalate)
    )

    analytics.log_query(
        persona,
        user_query,
        escalate
    )

    # ----------------------------------
    # ASSISTANT RESPONSE
    # ----------------------------------

    with st.chat_message("assistant"):

        st.markdown(response)

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Detected Persona",
                persona
            )

        with col2:

            st.metric(
                "Confidence",
                f"{confidence:.2f}"
            )

        with col3:

            st.metric(
                "Sources Found",
                len(docs)
            )

        st.divider()

        st.subheader(
            "📚 Retrieved Knowledge Sources"
        )

        if docs:

            for doc in docs:

                with st.expander(
                    f"{doc['source']} | Confidence {doc['confidence']}"
                ):

                    st.write(
                        doc["content"]
                    )

        else:

            st.warning(
                "No relevant sources found."
            )

        st.divider()

        # --------------------------
        # ESCALATION PANEL
        # --------------------------

        if escalate:

            st.error(
                f"🚨 Escalation Triggered: {reason}"
            )

            summary = handoff.generate(
                persona=persona,
                issue=user_query,
                conversation_history=memory.get_history(
                    st.session_state.session_id
                ),
                documents_used=[
                    d["source"]
                    for d in docs
                ],
                attempted_steps=[
                    "Knowledge Base Retrieval",
                    "AI Response Generation"
                ],
                recommendation=
                "Human Support Agent Review Required"
            )

            st.subheader(
                "👨‍💼 Human Handoff Summary"
            )

            st.code(
                summary,
                language="json"
            )

        else:

            st.success(
                "✅ No Escalation Required"
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ==========================================
# FEEDBACK SECTION
# ==========================================

st.divider()

st.subheader(
    "⭐ Feedback"
)

rating = st.slider(
    "Rate this support experience",
    min_value=1,
    max_value=5,
    value=5
)

comments = st.text_area(
    "Additional Comments"
)

if st.button(
    "Submit Feedback"
):

    feedback_manager.save_feedback(
        rating,
        comments
    )

    st.success(
        "Feedback saved successfully."
    )