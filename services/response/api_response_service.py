import uuid


def success_response(
    data: dict
):

    """
    Standardized success API response.
    """

    return {
        "success": True,
        "request_id": str(uuid.uuid4()),
        "data": data
    }


def error_response(
    error_type: str,
    message: str
):

    """
    Standardized error API response.
    """

    return {
        "success": False,
        "request_id": str(uuid.uuid4()),
        "error": {
            "type": error_type,
            "message": message
        }
    }