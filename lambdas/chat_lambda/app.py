import json
import os
from http import HTTPStatus
from openai import OpenAI

import requests

from api import responses


# TODO: get from env/secrets
OPENAI_API_KEY = "<APIKEY>"

client = OpenAI(api_key=OPENAI_API_KEY)


def lambda_handler(event: dict, context) -> dict:
    """
    AWS Lambda handler function.

    Parameters:
        event (dict): The input event triggering the Lambda function.
        context: AWS Lambda execution context.

    Returns:
        dict: The Lambda response object.

    Example Usage:
        response = lambda_handler({"key": "value"}, None)
        print(response)
    """
    # searcher_url = os.getenv("SEARCHER_URL")
    # Make the POST request to the searcher service
    query = json.loads(event['body'])['query']
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
        return responses.default(HTTPStatus.OK, {"llm_response": llm_response})
    # Handle an error response
    return responses.default(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": response.json()})


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
