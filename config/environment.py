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
    return value