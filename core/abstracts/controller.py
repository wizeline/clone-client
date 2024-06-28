from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class AbstractMaskController(ABC):
    """
    Abstract class for main controller class.
    """

    @abstractmethod
    def mask(self, request: Dict[str, Any]) -> Tuple[Dict[str, str], int]:
        """
        Abstract method to handle vectorization requests.

        Args:
            request (Dict[str, Any]): Request body.

        Returns:
            Tuple[Dict[str, str], int]: Tuple containing a JSON response indicating success or failure of the vectorization process and an HTTP status code.
        """
        pass
