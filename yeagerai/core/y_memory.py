import os

from langchain.chat_models import ChatOpenAI

# from langchain.llms import OpenAI
from langchain.memory import (
    ConversationSummaryMemory,
    ConversationEntityMemory,
    CombinedMemory,
    RedisChatMessageHistory,
    ConversationBufferWindowMemory,
)


class YeagerExtendedMemory:
    pass


class YeagerContextMemory:
    """Memory for the Yeager agent."""

    def __init__(self, username: str, session_id: str, session_path: str):
        self.username = username
        self.session_id = session_id
        self.session_path = session_path

        self.session_history = RedisChatMessageHistory(session_id)

        self.last_messages_memory = ConversationBufferWindowMemory(
            k=10, memory_key="session_last_messages"
        )
        self.rolling_summary_session_memory = ConversationSummaryMemory(
            llm=ChatOpenAI(), memory_key="session_summary"
        )

        self.memory = CombinedMemory(
            memories=[
                self.last_messages_memory,
                self.rolling_summary_session_memory,
            ]
        )

    def load_or_create_session_history(self):
        try:
            self.session_history.messages = open(
                os.path.join(self.session_path, "session_history.txt"), "r"
            ).read()
        except FileNotFoundError:
            os.makedirs(
                os.path.join(self.session_path, "session_history.txt"), exist_ok=True
            )

    def store_session_history(self):
        with open(os.path.join(self.session_path, "session_history.txt"), "w") as f:
            f.write(self.session_history.messages)
        pass

    def load_last_messages(self):
        self.last_messages_memory.chat_memory = self.session_history.messages

    def load_summary(self):
        self.rolling_summary_session_memory.chat_memory = self.session_history.messages

    def load_memory(self):
        self.load_or_create_session_history()
        self.load_last_messages()
        self.load_summary()
