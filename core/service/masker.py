from logging import Logger
from typing import Any
from openai import OpenAI

from core.abstracts.services import AbstractMaskerService

class MaskerService(AbstractMaskerService):
    """
    Service class for Masker operations.
    """

    def __init__(self, openai_key: str, logger: Logger):
        """
        Initialize Masker Service.

        Args:
            openai_key (str): OpenAI API key
            logger (Logger): Logger instance.
        """

        self.client = OpenAI(api_key=openai_key)
        self.logger = logger

    def llm_query(self, query: str, documents: Any) -> str:
        """
        Performs a prompt to a LLM

        Args:
            query (str): Opensearch DSL query string

        Returns:
            dict: a dictionary with the opensearch query document results
        """

        rag_prompt = """
        Given the following information, please provide an answer that accurately summarizes the relevant documents and cites the appropriate sources.

        Query: {user_query}
        Documents:
        {document_list}
        Important:

        Directly quote any text from the documents used to formulate your answer.
        Cite the sources by referencing their "file_uuid" and "source_name".
        """
        prompt = rag_prompt.format(user_query=query, document_list=documents)
        # TODO: mask prompt
        llm_response = self.query_llm(prompt)
        # TODO: unmask response
        return llm_response

    def query_llm(self, prompt):
        # TODO: context maintenance (system message + previous conversation context, summarize session context for future conversations)
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
