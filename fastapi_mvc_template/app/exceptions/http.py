"""HTTP exception and handler for FastAPI."""
from typing import Any, Optional, Dict

from fastapi import Request
from fastapi.responses import JSONResponse


class HTTPException(Exception):
    """Custom HTTPException class definition.

    This exception combined with exception_handler method allows you to use it
    the same manner as you'd use FastAPI.HTTPException with one difference. You
    have freedom to define returned response body, where as in
    FastAPI.HTTPException content is returned under "detail" JSON key.

    FastAPI.HTTPException source:
    https://github.com/tiangolo/fastapi/blob/master/fastapi/exceptions.py

    """

    def __init__(
        self,
        status_code: int,
        content: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize HTTPException class object instance.

        Args:
            status_code(int): HTTP error status code.
            content(Any): Response body.
            headers(Optional[Dict[str, Any]]): Additional response headers.

        """
        self.status_code = status_code
        self.content = content
        self.headers = headers

    def __repr__(self):
        """Class custom __repr__ method implementation.

        Returns:
            str: HTTPException string object.

        """
        kwargs = []

        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                kwargs.append(
                    "{key}={value}".format(
                        key=key,
                        value=repr(value)
                    )
                )

        return "{name}({kwargs})".format(
            name=self.__class__.__name__,
            kwargs=", ".join(kwargs)
        )


async def http_exception_handler(request: Request, exception: HTTPException):
    """Handle HTTPException globally.

    In this application custom handler is added in asgi.py while initializing
    FastAPI application. This is needed in order to handle custom HTTException
    globally.

    More details:
    https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers

    Args:
        request(starlette.requests.Request): Request class object instance.
            More details: https://www.starlette.io/requests/
        exception(HTTPException): Custom HTTPException class object instance.

    Returns:
        FastAPI.response.JSONResponse class object instance initialized with
            kwargs from custom HTTPException.

    """
    return JSONResponse(
        status_code=exception.status_code,
        content=exception.content,
        headers=exception.headers,
    )