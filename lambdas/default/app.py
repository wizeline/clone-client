from http import HTTPStatus

from api import responses


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
    return responses.Lambda(HTTPStatus.OK, {"message": "hello world"})
