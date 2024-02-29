import json
from typing import Any, Dict


def Lambda(code: int, body: Dict[str, Any]) -> dict:
    """
    Generate a response object for AWS Lambda functions.

    Parameters:
        code (int): HTTP status code.
        body (any): Response body.

    Returns:
        dict: Response object with "statusCode" and "body" keys.
    """
    return {
        "statusCode": code,
        "body": json.dumps(body),
    }
