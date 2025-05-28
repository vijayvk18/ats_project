from rest_framework.response import Response


def api_response(code, message, data, status=None):
    """
    Common function to format API responses consistently

    Args:
        code (int): HTTP status code
        message (str): Response message
        data (dict/list): Response data
        status (str, optional): Custom status string. Defaults to None.

    Returns:
        Response: Formatted API response
    """
    response_data = {
        "status": status if status is not None else code,
        "message": message,
        "data": data,
    }
    return Response(data=response_data, status=code)
