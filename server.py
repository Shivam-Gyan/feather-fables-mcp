from fastmcp import FastMCP
from dotenv import load_dotenv
import mcp
from Tools.get_blog import get_blog
from Tools.blog_tools import save_to_draft_tool, user_written_blogs_tool
from Tools.user_tools import get_user_profile_tool, update_profile_tool, check_notification_tool
from schemas.blog.draft import SaveDraftInput, SaveDraftOutput
from schemas.blog.user_written_blogs import UserWrittenBlogsInput, UserWrittenBlogsOutput
from schemas.user.profile import UpdateProfileInput, UpdateProfileOutput

load_dotenv()


app = FastMCP(name="feather-fables-mcp", version="0.1.0")


@app.tool(name="test", description="Testing only.")
async def test():
    try:
        return await get_blog()
    except Exception as e:
        return f"Error fetching blog: {e}"


@app.tool(name="save_to_draft", description="Save a generated blog post to the Feather Fables website as a draft.")
async def accept_save_to_draft_tool(input: SaveDraftInput, access_token: str) -> SaveDraftOutput:
    try:
        return await save_to_draft_tool(input, access_token=access_token)
    except Exception as e:
        return SaveDraftOutput(
            message=f"Error saving draft: {e}",
            success=False,
            blog_id=None,
        )


@app.tool(name="get_user_profile_info", description="Get user profile information.")
async def accept_get_user_profile_info_tool(access_token: str):
    """Get user profile information."""
    try:
        return await get_user_profile_tool(access_token=access_token)
    
    except Exception as e:
        return f"Error fetching user profile: {e}"


@app.tool(name="update_profile", description="Update user profile information (username, bio, social links).")
async def accept_update_profile_tool(input: UpdateProfileInput, access_token: str) -> UpdateProfileOutput:
    """Update user profile on the Feather Fables server."""
    try:
        return await update_profile_tool(input, access_token=access_token)
    except Exception as e:
        return UpdateProfileOutput(
            success=False,
            message=f"Error updating profile: {e}",
            username=None,
        )


@app.tool(name="check_notification", description="Check if the user has any new unread notifications.")
async def accept_check_notification_tool(access_token: str):
    """Check for new notifications."""
    try:
        return await check_notification_tool(access_token=access_token)
    except Exception as e:
        return {"new_notification": False, "error": str(e)}


@app.tool(name="user_written_blogs", description="Fetch paginated list of blogs written by the authenticated user, with optional title search and draft filtering.")
async def accept_user_written_blogs_tool(input: UserWrittenBlogsInput, access_token: str) -> UserWrittenBlogsOutput:
    """Fetch user-written blogs with pagination and search."""
    try:
        return await user_written_blogs_tool(input, access_token=access_token)
    except Exception as e:
        return UserWrittenBlogsOutput(
            success=False,
            message=f"Error fetching user written blogs: {e}",
            docs=[],
        )


if __name__ == "__main__":
    app.run()