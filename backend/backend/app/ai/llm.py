from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app.core.config import HF_TOKEN


class LLMService:

    def __init__(self):

        endpoint = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-7B-Instruct",
            huggingfacehub_api_token=HF_TOKEN,
            task="conversational",
            max_new_tokens=512,
            temperature=0.2,
        )

        self.llm = ChatHuggingFace(
            llm=endpoint
        )

    def generate(self, prompt: str):

        response = self.llm.invoke(prompt)

        return response.content


llm_service = LLMService()