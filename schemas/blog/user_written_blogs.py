"""Pydantic schemas for fetching user-written blogs."""

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class UserWrittenBlogsInput(BaseModel):
    """Input schema for retrieving a user's written blog posts."""

    model_config = ConfigDict(strict=True, extra="forbid")

    page: int = Field(
        default=1,
        description="Page number for pagination (1-indexed).",
        ge=1,
    )
    draft: bool = Field(
        ...,
        description="If True, fetch drafts; if False, fetch published blogs.",
    )
    query: str = Field(
        default="",
        description="Search query to filter blogs by title (case-insensitive).",
        max_length=200,
    )
    deleted_doc_count: int = Field(
        default=0,
        description="Number of documents deleted in the current session, used to adjust pagination offset.",
        ge=0,
    )


class BlogDocument(BaseModel):
    """Schema representing a single blog document in the response."""

    model_config = ConfigDict(extra="allow")

    title: str = Field(..., description="Title of the blog post.")
    banner: Optional[str] = Field(default=None, description="Banner image URL.")
    publishedAt: Optional[str] = Field(default=None, description="ISO timestamp when the blog was published.")
    blog_id: str = Field(..., description="Unique identifier for the blog post.")
    activity: Optional[dict] = Field(default=None, description="Activity stats (likes, comments, reads, etc.).")
    des: Optional[str] = Field(default=None, description="Short description of the blog post.")
    draft: bool = Field(default=False, description="Whether the blog is a draft.")


class UserWrittenBlogsOutput(BaseModel):
    """Output schema for the user-written blogs operation."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(..., description="Whether the operation succeeded.")
    message: str = Field(..., description="Human-readable result message.")
    docs: List[BlogDocument] = Field(
        default_factory=list,
        description="List of blog documents matching the query.",
    )
