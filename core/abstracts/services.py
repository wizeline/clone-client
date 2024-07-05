from abc import ABC, abstractmethod
from typing import Any, Dict


class AbstractMaskerService(ABC):
    """
    Abstract class for main controller class.
    """

    @abstractmethod
    def llm_query(self, query: str, documents: Any) -> str:
        """
        """
        pass

class AbstractOpenSearchService(ABC):
    """
    Abstract class for main controller class.
    """

    @abstractmethod
    def request(self, query: str) -> Dict[str, Any]:
        """
        """
        pass
