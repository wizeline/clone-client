from http import HTTPStatus
from logging import Logger
from typing import Any, Dict, Tuple

from flask import Response, jsonify

from core.abstracts.controller import AbstractCloneClientController
from core.abstracts.usecases import AbstractCloneClientUsecase


class CloneClientController(AbstractCloneClientController):
    """
    Controller for Clone Client operations.
    """

    def __init__(self, usecase: AbstractCloneClientUsecase, logger: Logger):
        """
        Initialize the Controller.

        Args:
            usecase (AbstractCloneClientUsecase): An instance of a class implementing the AbstractCloneClientUsecase interface.
        """

        self.logger = logger
        self.usecase = usecase

    async def chat(self, request: Dict[str, Any]) -> Tuple[Response, int]:
        """
        Handle clone client requests.

        This method expects a POST request with JSON data containing the query to look for documents in Open Search

        Args:
            request (Dict[str, Any]): Request body.

        Returns:
            Tuple[Dict[str, str], int]: Tuple containing a JSON response indicating the status of the search and masking process and an HTTP status code.
        """

        # TODO: get JWT from headers, validate
        # TODO: refactor chat endpoint to /v1/<clone-UUID>/chat
        # TODO: retrieve data for <clone-uuid> (system message, previous context, project details)
        # searcher_url = os.getenv("SEARCHER_URL")
        # Make the POST request to the searcher service
        query = request["query"]

        try:
            response = await self.usecase.chat(query)
            return jsonify({"llm_response": response}, HTTPStatus.OK)
        except Exception as e:
            self.logger.error(e)
            return jsonify({"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR)
