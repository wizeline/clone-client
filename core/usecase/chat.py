from logging import Logger

from core.abstracts.usecases import AbstractCloneClientUsecase
from core.abstracts.services import AbstractMaskerService, AbstractOpenSearchService


class CloneClientUsecase(AbstractCloneClientUsecase):
    """
    Controller for CloneClient operations.
    """

    def __init__(self, masker: AbstractMaskerService, searcher: AbstractOpenSearchService, logger: Logger):
        """
        Initialize Clone Client.

        Args:
            masker (AbstractMaskerService): An instance of a class implementing the AbstractMaskerService interface.
            searcher (AbstractOpenSearchService): An instance of a class implementing the AbstractOpenSearchService interface.
            logger (Logger): Logger instance.
        """

        self.logger = logger
        self.masker = masker
        self.searcher = searcher

    def chat(self, query: str) -> str:
        """
        This method requests documents related to a query and mask sensitive data

        Args:
            query (str): Opensearch DSL query string

        Returns:
            str: the response of the LLM prompt
        """

        search_result = self.searcher.request(query)

        if "results" not in search_result:
            self.logger.error({"data": search_result, "error": "no result in response"})
            raise Exception("no result in response")

        documents = search_result["results"]
        llm_response = self.masker.llm_query(query, documents)
        return llm_response
