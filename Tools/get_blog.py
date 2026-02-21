from config.environment import get_env_variable


async def get_blog() -> str:
    """
    Get the latest blog post from the website.

    Returns:
        str: The content of the latest blog post.

    Raises:
        ValueError: If the ACCESS_TOKEN environment variable is not set.
    """
    try:
        access_token = get_env_variable("ACCESS_TOKEN")
        return f"This is the latest blog post with access token: {access_token}."
    except ValueError as e:
        raise ValueError(f"Failed to retrieve blog: {e}") from e