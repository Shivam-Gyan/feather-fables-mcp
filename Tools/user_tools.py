

from config.environment import get_env_variable
from request.http import get, patch
from schemas.user.profile import UpdateProfileInput, UpdateProfileOutput
from dotenv import load_dotenv
load_dotenv()
import os

os.environ["PORT"] = os.getenv("PORT", "8000")


URL = os.getenv("SERVER_URL_FF","http://localhost:8080/api/v1/mcp") 
os.environ["SERVER_URL_FF"] = URL + "/api/v1/mcp"

async def get_user_profile_tool(access_token: str):

    try:
        response = await get(
            url=f"{get_env_variable('SERVER_URL_FF')}/user/get-user-profile-info",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return response.json()
    
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve user profile: {e}") from e


async def update_profile_tool(input: UpdateProfileInput, access_token: str) -> UpdateProfileOutput:
    """
    Update user profile on the Feather Fables server.

    Args:
        input: The profile data to update (username, bio, social_links).
        access_token: Bearer token for authentication.

    Returns:
        UpdateProfileOutput: The result of the update operation.

    Raises:
        RuntimeError: If an unexpected error occurs during the update.
    """
    try:
        response = await patch(
            url=f"{get_env_variable('SERVER_URL_FF')}/user/update-profile",
            json={
                "username": input.username,
                "bio": input.bio,
                "social_links": input.social_links.model_dump(),
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        data = response.json()

        return UpdateProfileOutput(
            success=data.get("success", True),
            message=data.get("message", "Profile updated."),
            username=data.get("username", input.username),
        )

    except Exception as e:
        raise RuntimeError(f"Failed to update profile: {e}") from e


async def check_notification_tool(access_token: str) -> dict:
    """
    Check if the user has any new unread notifications.

    Args:
        access_token: Bearer token for authentication.

    Returns:
        dict: {"new_notification": bool}

    Raises:
        RuntimeError: If an unexpected error occurs.
    """
    try:
        response = await get(
            url=f"{get_env_variable('SERVER_URL_FF')}/user/check-any-notification",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return response.json()

    except Exception as e:
        raise RuntimeError(f"Failed to check notifications: {e}") from e
    

