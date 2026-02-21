"""Pydantic schemas for fetching a blog by its ID."""

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, List, Optional

from schemas.blog.common import BlogAuthor


class GetBlogByIdInput(BaseModel):
    """Input schema for retrieving a blog post by its blog_id."""

    model_config = ConfigDict(strict=True, extra="forbid")

    blog_id: str = Field(
        ...,
        description="Unique identifier of the blog post to retrieve.",
        min_length=1,
    )
    draft: bool = Field(
        default=False,
        description="Set to True if you intend to access a draft blog.",
    )
    mode: str = Field(
        default="read",
        description="Access mode: 'read' increments read count, 'edit' does not.",
    )


class GetBlogByIdOutput(BaseModel):
    """Output schema for the get-blog-by-id operation."""

    model_config = ConfigDict(extra="allow")

    success: bool = Field(default=True, description="Whether the operation succeeded.")
    title: Optional[str] = Field(default=None, description="Title of the blog post.")
    des: Optional[str] = Field(default=None, description="Short description of the blog post.")
    content: Optional[Any] = Field(default=None, description="Blog content (editor blocks).")
    banner: Optional[str] = Field(default=None, description="Banner image URL.")
    activity: Optional[Dict[str, Any]] = Field(default=None, description="Activity stats (total_reads, total_likes, etc.).")
    publishedAt: Optional[str] = Field(default=None, description="ISO timestamp when the blog was published.")
    blog_id: Optional[str] = Field(default=None, description="Unique identifier of the blog post.")
    tags: Optional[List[str]] = Field(default=None, description="Tags associated with the blog post.")
    author: Optional[BlogAuthor] = Field(default=None, description="Author information.")
    message: Optional[str] = Field(default=None, description="Human-readable result or error message.")
