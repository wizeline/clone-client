import json
from logging import Logger
from typing import Any, Dict

import requests

from core.abstracts.services import AbstractOpenSearchService


class OpenSearchService(AbstractOpenSearchService):
    """
    Service class for Opensearch operations.
    """

    def __init__(self, searcher_url: str, logger: Logger):
        """
        Initialize OpenSearch Client Service.

        Args:
            searcher_url (str): Opensearch URL service
            logger (Logger): Logger instance.
        """

        self.logger = logger
        self.searcher_url = searcher_url

    def request(self, query: str) -> Dict[str, Any]:
        """
        Performs a request to OpenSearch

        Args:
            query (str): Opensearch DSL query string

        Returns:
            dict: a dictionary with the opensearch query document results
        """

        data = {"q": query}
        response = requests.post(
            self.searcher_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
        )
        if response.status_code != 200:
            self.logger.error({"searcher_status_code": response.status_code})
            raise Exception(response.json())
        return response.json()
