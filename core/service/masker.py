import json
from dataclasses import field
from logging import Logger
from typing import Any, Optional

from openai import OpenAI

from core.abstracts.services import AbstractMaskerService
from core.service.masks import MaskBase


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
        self._mask_lookup = {}
        self.masked_data: str | list = field(init=False)
        self.skip: Optional[list] = None

    async def llm_query(self, query: str, documents: Any) -> str:
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
        prompt = await self.mask_data(prompt)
        llm_response = self.query_llm(prompt)
        llm_response = self.unmask_data(llm_response)
        return llm_response

    def query_llm(self, prompt):
        # TODO: context maintenance (system message + previous conversation context, summarize session context for future conversations)
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content

    async def mask_data(self, data_to_mask: list[str]):
        if isinstance(data_to_mask, list):
            aux = [message.model_dump() for message in data_to_mask]
            data: str = json.dumps(aux)
        else:
            data = data_to_mask

        for mask in MaskBase.__subclasses__():
            if self.skip and mask.__name__ in self.skip:
                if self.debug:
                    self.logger.info(f"Skipping mask {mask.__name__}")

                continue

            to_mask = await mask.find(data)
            for i, item in enumerate(to_mask):
                if item not in self._mask_lookup.values():
                    lookup_name = f"<{mask.__name__}_{i + 1}>"
                    print(f"mask: {lookup_name}, item: {item}")
                    self._mask_lookup[lookup_name] = item
                    data = data.replace(item, lookup_name)

        if isinstance(data_to_mask, list):
            data = json.loads(data)
        return data

    def unmask_data(self, data: str) -> str:
        unmasked = data
        for k, v in self._mask_lookup.items():
            unmasked = unmasked.replace(k, v)
        return unmasked

    def list_masks(self) -> list[str]:
        return [mask.__name__ for mask in MaskBase.__subclasses__()]

    def get_lookup(self) -> dict:
        return self._mask_lookup
