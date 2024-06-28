from http import HTTPStatus
from logging import Logger
from typing import Any, Dict, Tuple
from openai import OpenAI

import json
import requests

from flask import jsonify, Response

from core.abstracts.controller import AbstractMaskController


# TODO: get from env/secrets
OPENAI_API_KEY = "<APIKEY>"

client = OpenAI(api_key=OPENAI_API_KEY)

class MaskController(AbstractMaskController):
    """
    Controller for vectorization operations.
    """

    def __init__(self, logger: Logger):
        """
        Initialize the Controller.

        Args:
            usecase (AbstractUsecase): An instance of a class implementing the AbstractUsecase interface.
        """
        self.logger = logger

    def mask(self, request: Dict[str, Any]) -> Tuple[Response, int]:
        """
        Handle vectorization requests.

        This method expects a POST request with JSON data containing S3 bucket and object key information.
        It delegates vectorization and indexing tasks to the use case, and returns appropriate responses.

        Args:
            request (Dict[str, Any]): Request body.

        Returns:
            Tuple[Dict[str, str], int]: Tuple containing a JSON response indicating success or failure of the vectorization process and an HTTP status code.
        """
        # TODO: get JWT from headers, validate
        # TODO: refactor chat endpoint to /v1/<clone-UUID>/chat
        # TODO: retrieve data for <clone-uuid> (system message, previous context, project details)
        # searcher_url = os.getenv("SEARCHER_URL")
        # Make the POST request to the searcher service
        query = request['query']
        data = {
            "q": query
        }
        response = requests.post(
            'http://host.docker.internal:8000/v1/api/search',
            # searcher_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )

        # Handle the response
        if response.status_code == 200:
            # Process the successful response
            result = response.json()
            documents = result["results"]
            llm_response = llm_query(query, documents)
            return jsonify({"llm_response": llm_response}, HTTPStatus.OK)
        # Handle an error response
        return jsonify({"error": response.json()}, HTTPStatus.INTERNAL_SERVER_ERROR)


def llm_query(query, documents):
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
    llm_response = query_llm(prompt)
    # TODO: unmask response
    return llm_response


def query_llm(prompt):
    # TODO: context maintenance (system message + previous conversation context, summarize session context for future conversations)
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content
