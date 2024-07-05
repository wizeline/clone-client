from abc import ABC, abstractmethod


class AbstractCloneClientUsecase(ABC):
    """
    Abstract class for main controller class.
    """

    @abstractmethod
    def chat(self, query: str) -> str:
        """
        Abstract method to handle vectorization requests.

        Args:
            request (Dict[str, Any]): Request body.

        Returns:
            Tuple[Dict[str, str], int]: Tuple containing a JSON response indicating success or failure of the vectorization process and an HTTP status code.
        """
        pass
