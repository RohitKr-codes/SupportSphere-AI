from collections import deque


class ConversationMemory:

    def __init__(
        self,
        max_history=10
    ):

        self.max_history = max_history

        self.memory = {}

    def add_message(
        self,
        session_id,
        role,
        content
    ):

        if session_id not in self.memory:

            self.memory[session_id] = deque(
                maxlen=self.max_history
            )

        self.memory[session_id].append(
            {
                "role": role,
                "content": content
            }
        )

    def get_history(
        self,
        session_id
    ):

        return list(
            self.memory.get(
                session_id,
                []
            )
        )

    def clear(
        self,
        session_id
    ):

        if session_id in self.memory:
            del self.memory[session_id]