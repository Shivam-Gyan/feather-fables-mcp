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
from schemas.blog.get_blog_by_id import GetBlogByIdInput, GetBlogByIdOutput
from schemas.blog.search_blogs import SearchBlogsInput, SearchBlogsOutput, SearchBlogItem
from request.http import post

# from dotenv import load_dotenv
# load_dotenv()
import os

# os.environ["PORT"] = os.getenv("PORT", "8000")

# URL = os.getenv("SERVER_URL_FF","http://localhost:8080/api/v1/mcp") 
# os.environ["SERVER_URL_FF"] = URL + "/api/v1/mcp"
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


async def get_blog_by_id_tool(input: GetBlogByIdInput, access_token: str) -> GetBlogByIdOutput:
    """
    Fetch a single blog post by its blog_id.

    When mode is 'read', the server increments the total read count
    for both the blog and the author. When mode is 'edit', reads are
    not incremented. Draft blogs can only be accessed when draft=True.

    Args:
        input (GetBlogByIdInput): blog_id, draft flag, and access mode.
        access_token: Bearer token for authentication.

    Returns:
        GetBlogByIdOutput: The full blog document with author info.

    Raises:
        RuntimeError: If an unexpected error occurs during the fetch.
    """
    try:
        response = await post(
            url=f"{get_env_variable('SERVER_URL_FF')}/blog/get-blog",
            json={
                "blog_id": input.blog_id,
                "draft": input.draft,
                "mode": input.mode,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        data = response.json()

        return GetBlogByIdOutput(success=True, **data)

    except Exception as e:
        raise RuntimeError(f"Failed to fetch blog by id: {e}") from e


async def search_blogs_tool(input: SearchBlogsInput, access_token: str) -> SearchBlogsOutput:
    """
    Search published blogs by tag, title query, or author.

    Supports pagination and an optional blog_id to exclude from results
    (useful when showing related posts on a currently open blog).

    Args:
        input (SearchBlogsInput): Search filters, pagination, and limit.
        access_token: Bearer token for authentication.

    Returns:
        SearchBlogsOutput: The list of matching blog posts.

    Raises:
        RuntimeError: If an unexpected error occurs during the search.
    """
    try:
        body: dict = {"page": input.page}

        if input.tag is not None:
            body["tag"] = input.tag
        if input.query is not None:
            body["query"] = input.query
        if input.author is not None:
            body["author"] = input.author
        if input.limit is not None:
            body["limit"] = input.limit
        if input.eliminate_blog is not None:
            body["eliminate_blog"] = input.eliminate_blog

        response = await post(
            url=f"{get_env_variable('SERVER_URL_FF')}/blog/search-blogs",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        data = response.json()

        blogs = [SearchBlogItem(**b) for b in data.get("blogs", [])]

        return SearchBlogsOutput(
            success=True,
            message=f"Found {len(blogs)} blog(s).",
            blogs=blogs,
        )

    except Exception as e:
        raise RuntimeError(f"Failed to search blogs: {e}") from e
