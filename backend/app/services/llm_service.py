from langchain_huggingface import HuggingFaceEndpoint

from app.core.config import HF_TOKEN


class LLMService:
    """
    Singleton service responsible for all LLM interactions.
    """

    def __init__(self):
        self.llm = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-7B-Instruct",
            huggingfacehub_api_token=HF_TOKEN,
            task="text-generation",
            max_new_tokens=512,
            temperature=0.2,
            do_sample=False,
        )

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.2,
    ) -> str:

        self.llm.max_new_tokens = max_tokens
        self.llm.temperature = temperature

        response = self.llm.invoke(prompt)

        return response


# Singleton instance
llm_service = LLMService()