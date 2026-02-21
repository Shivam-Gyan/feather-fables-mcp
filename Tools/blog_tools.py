"""
Save a generated blog post to the Feather Fables website as a draft.

An AI agent generates the blog content, then calls this tool
to submit it to the drafts section on the Feather Fables server.
The tool takes the generated blog content as input and sends it to the server   
to be saved as a draft. The server will then store the draft and make it available
for further editing and eventual publication by the human team at Feather Fables website.
"""



from config.environment import get_env_variable
from schemas.blog.draft import SaveDraftInput, SaveDraftOutput
from schemas.blog.user_written_blogs import UserWrittenBlogsInput, UserWrittenBlogsOutput, BlogDocument
from request.http import post


# This Function use to save the generated blog by Agentic AI to draft in feather fables webserver.
async def save_to_draft_tool(input: SaveDraftInput,access_token:str) -> SaveDraftOutput:
    """
    Save a generated blog post to the Feather Fables website as a draft.

    Args:
        input (SaveDraftInput): The input data for saving the blog post as a draft.

    Returns:
        SaveDraftOutput: The result of the save operation.

    Raises:
        RuntimeError: If an unexpected error occurs during the save.
    """
    try:
        # Placeholder: send input data to the Feather Fables server.
        response = await post(
            url=f"{get_env_variable('SERVER_URL_FF')}/blog/auto-blog",
            json={
                "title": input.title,
                "markdown": input.markdown,
                "tags": input.tags,
                "description": input.description,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        data = response.json()

        return SaveDraftOutput(
            message= data.get("message", f"Blog post titled '{input.title}' has been saved as a draft with tags {input.tags}."),
            success=data.get("success", True),
            blog_id=data.get("blog_id"),
        )
    

    except Exception as e:
        raise RuntimeError(f"Failed to save draft: {e}") from e
    


async def user_written_blogs_tool(input: UserWrittenBlogsInput, access_token: str) -> UserWrittenBlogsOutput:
    """
    Fetch paginated list of blogs written by the authenticated user.

    Supports filtering by draft status and title search query.
    Pagination offset is adjusted when documents have been deleted in the current session.

    Args:
        input (UserWrittenBlogsInput): Pagination, draft flag, search query, and deleted doc count.
        access_token: Bearer token for authentication.

    Returns:
        UserWrittenBlogsOutput: The list of matching blog documents.

    Raises:
        RuntimeError: If an unexpected error occurs during the fetch.
    """
    try:
        response = await post(
            url=f"{get_env_variable('SERVER_URL_FF')}/blog/user-written-blogs",
            json={
                "page": input.page,
                "draft": input.draft,
                "query": input.query,
                "deletedDocCount": input.deleted_doc_count,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        data = response.json()

        docs = [BlogDocument(**doc) for doc in data.get("docs", [])]

        return UserWrittenBlogsOutput(
            success=data.get("success", True),
            message=data.get("message", f"Found {len(docs)} blog(s)."),
            docs=docs,
        )

    except Exception as e:
        raise RuntimeError(f"Failed to fetch user written blogs: {e}") from e
