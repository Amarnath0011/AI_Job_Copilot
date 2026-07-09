from langchain_classic.output_parsers.fix import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser

from app.services.llm_service import llm_service


class LLMParser:
    """
    Utility class responsible for parsing LLM outputs.

    Workflow:
    1. Try normal Pydantic parsing.
    2. If parsing fails, use OutputFixingParser.
    """

    @staticmethod
    def parse(
        response: str,
        parser: PydanticOutputParser,
    ):
        try:
            return parser.parse(response)

        except Exception:

            fixing_parser = OutputFixingParser.from_llm(
                parser=parser,
                llm=llm_service.llm,
            )

            return fixing_parser.parse(response)