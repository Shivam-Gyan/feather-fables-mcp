import os

from dotenv import load_dotenv

load_dotenv()


def get_env_variable(name: str) -> str:
    """Get an environment variable by name.

    Args:
        name: The name of the environment variable.

    Returns:
        The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set.
    """
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set.")
    # Normalize common duplication mistakes and trailing slashes so callers
    # that append endpoint paths don't accidentally produce duplicate segments.
    # Example: http://host/api/v1/mcp/api/v1/mcp -> http://host/api/v1/mcp
    value = value.rstrip('/')
    value = value.replace('/api/v1/mcp/api/v1/mcp', '/api/v1/mcp')
    return value