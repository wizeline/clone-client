from abc import ABC, abstractmethod
from typing import Any, Dict


class AbstractMaskerService(ABC):
    """
    Abstract class for AI services
    """

    @abstractmethod
    async def llm_query(self, query: str, documents: Any) -> str:
        """
        Abstract method to perform a prompt to a LLM

        Args:
            query (str): Opensearch DSL query string

        Returns:
            dict: a dictionary with the opensearch query document results
        """
        pass


class AbstractOpenSearchService(ABC):
    """
    Abstract class for Open Search services
    """

    @abstractmethod
    def request(self, query: str) -> Dict[str, Any]:
        """
        Abstract method to perform a request to OpenSearch

        Args:
            query (str): Opensearch DSL query string

        Returns:
            dict: a dictionary with the opensearch query document results
        """
        pass
