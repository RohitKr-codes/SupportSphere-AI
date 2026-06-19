import google.generativeai as genai

from src.config import Config


class ResponseGenerator:

    def __init__(self):

        genai.configure(
            api_key=Config.GEMINI_API_KEY
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def _persona_instruction(
        self,
        persona
    ):

        instructions = {

            "Technical Expert":
            """
            Respond as a technical support engineer.

            Include:
            - Root cause analysis
            - Technical explanation
            - Troubleshooting steps
            - Configuration guidance

            Be detailed and professional.
            """,

            "Frustrated User":
            """
            Respond with empathy.

            Requirements:
            - Acknowledge frustration
            - Use simple language
            - Give step-by-step actions
            - Focus on resolution

            Be supportive and reassuring.
            """,

            "Business Executive":
            """
            Respond concisely.

            Focus on:
            - Business impact
            - Service implications
            - Resolution timeline
            - Recommended actions

            Avoid unnecessary technical jargon.
            """
        }

        return instructions.get(
            persona,
            instructions[
                "Business Executive"
            ]
        )

    def _fallback_response(
        self,
        persona,
        retrieved_docs
    ):

        if not retrieved_docs:

            return """
⚠️ AI generation is temporarily unavailable.

I could not find relevant information in the knowledge base.

Please contact a human support representative for further assistance.
"""

        best_doc = max(
            retrieved_docs,
            key=lambda x: x["confidence"]
        )

        return f"""
⚠️ AI generation is temporarily unavailable.

Knowledge Base Match Found

Source: {best_doc['source']}
Page: {best_doc['page']}
Confidence: {best_doc['confidence']}

Relevant Information:

{best_doc['content']}

This response was generated using the local knowledge base fallback system.
"""

    def generate_response(
        self,
        user_query,
        persona,
        retrieved_docs
    ):

        context = "\n\n".join(
            [
                doc["content"]
                for doc in retrieved_docs
            ]
        )

        prompt = f"""
You are Adsparkx AI Customer Support Agent.

STRICT RULES:

1. Use ONLY the supplied knowledge base context.

2. Never invent facts.

3. If information is missing, say:

"I could not find this information in the knowledge base."

4. Keep responses accurate and professional.

5. Adapt your tone based on the detected persona.

Detected Persona:
{persona}

Persona Instructions:
{self._persona_instruction(persona)}

Knowledge Base Context:
{context}

Customer Query:
{user_query}

Generate the best support response.
"""

        try:

            response = self.model.generate_content(
                prompt
            )

            if (
                hasattr(response, "text")
                and response.text
            ):

                return response.text

            return self._fallback_response(
                persona,
                retrieved_docs
            )

        except Exception as e:

            print(
                f"Gemini Error: {str(e)}"
            )

            return self._fallback_response(
                persona,
                retrieved_docs
            )