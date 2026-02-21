"""Pydantic schemas for searching/filtering published blogs."""

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Any, Dict, List, Optional

from schemas.blog.common import BlogAuthor


class SearchBlogsInput(BaseModel):
    """Input schema for searching blogs by tag, title query, or author.

    Exactly one of `tag`, `query`, or `author` must be provided.
    """

    model_config = ConfigDict(strict=True, extra="forbid")

    tag: Optional[str] = Field(
        default=None,
        description="Filter blogs by this tag (returns published, non-draft blogs with matching tag).",
    )
    query: Optional[str] = Field(
        default=None,
        description="Search blogs by title (case-insensitive regex match).",
        max_length=200,
    )
    author: Optional[str] = Field(
        default=None,
        description="Filter blogs by author ID.",
    )
    page: int = Field(
        default=1,
        description="Page number for pagination (1-indexed).",
        ge=1,
    )
    limit: Optional[int] = Field(
        default=None,
        description="Max number of blogs to return per page. Defaults to 2 on the server if not provided.",
        ge=1,
        le=50,
    )
    eliminate_blog: Optional[str] = Field(
        default=None,
        description="blog_id to exclude from results (used when filtering by tag to hide the currently open blog).",
    )

    @model_validator(mode="after")
    def at_least_one_filter(self) -> "SearchBlogsInput":
        if not self.tag and not self.query and not self.author:
            raise ValueError("At least one of 'tag', 'query', or 'author' must be provided.")
        return self


class SearchBlogItem(BaseModel):
    """A single blog entry returned from the search endpoint."""

    model_config = ConfigDict(extra="allow")

    blog_id: str = Field(..., description="Unique identifier of the blog post.")
    title: Optional[str] = Field(default=None, description="Title of the blog post.")
    des: Optional[str] = Field(default=None, description="Short description of the blog post.")
    activity: Optional[Dict[str, Any]] = Field(default=None, description="Activity stats (likes, reads, etc.).")
    banner: Optional[str] = Field(default=None, description="Banner image URL.")
    tags: Optional[List[str]] = Field(default=None, description="Tags associated with the blog.")
    publishedAt: Optional[str] = Field(default=None, description="ISO timestamp when the blog was published.")
    author: Optional[BlogAuthor] = Field(default=None, description="Populated author info.")


class SearchBlogsOutput(BaseModel):
    """Output schema for the search-blogs operation."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(default=True, description="Whether the operation succeeded.")
    message: Optional[str] = Field(default=None, description="Human-readable result or error message.")
    blogs: List[SearchBlogItem] = Field(
        default_factory=list,
        description="List of blog posts matching the search criteria.",
    )
