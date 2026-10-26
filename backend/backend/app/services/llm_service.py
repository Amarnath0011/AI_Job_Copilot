from typing import Union

from langchain_core.messages import BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_groq import ChatGroq

from app.core.config import GROQ_API_KEY, GROQ_MODEL


class LLMService:
    """
    Singleton service responsible for all LLM interactions.
    Supports:
    - String prompts
    - PromptValue
    - Chat messages
    """

    def __init__(self):
        self.llm = ChatGroq(
            model=GROQ_MODEL,
            api_key=GROQ_API_KEY,
            temperature=0.2,
            max_tokens=1200,
        )

    def generate(
        self,
        prompt: Union[str, PromptValue, list[BaseMessage]],
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt:
                - str
                - PromptValue
                - list[BaseMessage]

        Returns:
            Generated text.
        """

        response = self.llm.invoke(prompt)

        return response.content.strip()


llm_service = LLMService()