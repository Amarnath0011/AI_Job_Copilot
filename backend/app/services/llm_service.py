from langchain_groq import ChatGroq

from app.core.config import GROQ_API_KEY


class LLMService:
    """
    Singleton service responsible for all LLM interactions.
    """

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=GROQ_API_KEY,
            temperature=0.2,
            max_tokens=700,
        )

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: Input prompt.

        Returns:
            Generated text as a string.
        """

        response = self.llm.invoke(prompt)

        # ChatGroq returns an AIMessage object.
        return response.content.strip()


# Singleton instance
llm_service = LLMService()