"""Universal async HTTP client for all outgoing API requests."""

import httpx
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Default timeout for all requests (seconds)
DEFAULT_TIMEOUT = 30.0


async def get(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> httpx.Response:
    """Send an async GET request.

    Args:
        url: The request URL.
        headers: Optional request headers.
        params: Optional query parameters.
        timeout: Request timeout in seconds.

    Returns:
        httpx.Response: The HTTP response.

    Raises:
        httpx.HTTPStatusError: If the response status code indicates an error.
        httpx.RequestError: If a network/connection error occurs.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.debug("GET %s", url)
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response


async def post(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> httpx.Response:
    """Send an async POST request.

    Args:
        url: The request URL.
        headers: Optional request headers.
        json: Optional JSON body.
        data: Optional form-encoded body.
        timeout: Request timeout in seconds.

    Returns:
        httpx.Response: The HTTP response.

    Raises:
        httpx.HTTPStatusError: If the response status code indicates an error.
        httpx.RequestError: If a network/connection error occurs.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.debug("POST %s", url)
        response = await client.post(url, headers=headers, json=json, data=data)
        response.raise_for_status()
        return response


async def put(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> httpx.Response:
    """Send an async PUT request.

    Args:
        url: The request URL.
        headers: Optional request headers.
        json: Optional JSON body.
        data: Optional form-encoded body.
        timeout: Request timeout in seconds.

    Returns:
        httpx.Response: The HTTP response.

    Raises:
        httpx.HTTPStatusError: If the response status code indicates an error.
        httpx.RequestError: If a network/connection error occurs.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.debug("PUT %s", url)
        response = await client.put(url, headers=headers, json=json, data=data)
        response.raise_for_status()
        return response


async def patch(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> httpx.Response:
    """Send an async PATCH request.

    Args:
        url: The request URL.
        headers: Optional request headers.
        json: Optional JSON body.
        data: Optional form-encoded body.
        timeout: Request timeout in seconds.

    Returns:
        httpx.Response: The HTTP response.

    Raises:
        httpx.HTTPStatusError: If the response status code indicates an error.
        httpx.RequestError: If a network/connection error occurs.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.debug("PATCH %s", url)
        response = await client.patch(url, headers=headers, json=json, data=data)
        response.raise_for_status()
        return response


async def delete(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> httpx.Response:
    """Send an async DELETE request.

    Args:
        url: The request URL.
        headers: Optional request headers.
        params: Optional query parameters.
        timeout: Request timeout in seconds.

    Returns:
        httpx.Response: The HTTP response.

    Raises:
        httpx.HTTPStatusError: If the response status code indicates an error.
        httpx.RequestError: If a network/connection error occurs.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.debug("DELETE %s", url)
        response = await client.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response
