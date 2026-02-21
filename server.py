from fastmcp import FastMCP
from dotenv import load_dotenv
from Tools.get_blog import get_blog
from Tools.blog_tools import save_to_draft_tool, user_written_blogs_tool, get_blog_by_id_tool, search_blogs_tool
from Tools.user_tools import get_user_profile_tool, update_profile_tool, check_notification_tool
from schemas.blog.draft import SaveDraftInput, SaveDraftOutput
from schemas.blog.user_written_blogs import UserWrittenBlogsInput, UserWrittenBlogsOutput
from schemas.blog.get_blog_by_id import GetBlogByIdInput, GetBlogByIdOutput
from schemas.blog.search_blogs import SearchBlogsInput, SearchBlogsOutput
from schemas.user.profile import UpdateProfileInput, UpdateProfileOutput

load_dotenv()
import os

os.environ["PORT"] = os.getenv("PORT", "8000")

URL = os.getenv("SERVER_URL_FF","http://localhost:8080/api/v1/mcp") 
os.environ["SERVER_URL_FF"] = URL + "/api/v1/mcp"


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


@app.tool(name="get_user_written_blogs", description="Fetch paginated list of blogs written by the authenticated user, with optional title search and draft filtering.")
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


@app.tool(name="get_blog_by_id", description="Fetch a single blog post by its unique blog_id. Increments read count unless mode is 'edit'.")
async def accept_get_blog_by_id_tool(input: GetBlogByIdInput, access_token: str) -> GetBlogByIdOutput:
    """Get a blog post by its blog_id."""
    try:
        return await get_blog_by_id_tool(input, access_token=access_token)
    except Exception as e:
        return GetBlogByIdOutput(
            success=False,
            message=f"Error fetching blog: {e}",
        )


@app.tool(name="search_blogs", description="Search published blogs by tag, title query, or author with pagination. Supports excluding a specific blog from results.")
async def accept_search_blogs_tool(input: SearchBlogsInput, access_token: str) -> SearchBlogsOutput:
    """Search blogs by tag, title, or author."""
    try:
        return await search_blogs_tool(input, access_token=access_token)
    except Exception as e:
        return SearchBlogsOutput(
            success=False,
            message=f"Error searching blogs: {e}",
            blogs=[],
        )


if __name__ == "__main__":
    app.run(transport="http", host="0.0.0.0", port=os.getenv("PORT", 8000))