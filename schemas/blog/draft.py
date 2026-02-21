"""Pydantic schemas for blog draft operations."""

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List


class SaveDraftInput(BaseModel):
    """Input schema for saving a blog post as a draft."""

    model_config = ConfigDict(strict=True, extra="forbid")

    title: str = Field(
        ...,
        description="Title of the blog post.",
        min_length=1,
        max_length=200,
    )
    markdown: str = Field(
        ...,
        description="Blog content in Markdown format.",
        min_length=1,
    )
    description: str = Field(
        ...,
        description="Short summary of the blog post.",
        max_length=500,
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for categorization.",
    )
    draft: bool = Field(
        default=True,
        description="Save as draft if True, publish if False.",
    )

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, v: list[str]) -> list[str]:
        """Strip whitespace and lowercase all tags, removing empty entries."""
        return [tag.strip().lower() for tag in v if tag.strip()]


class SaveDraftOutput(BaseModel):
    """Output schema for the save-draft operation."""

    model_config = ConfigDict(extra="forbid")

    message: str = Field(..., description="Human-readable result message.")
    success: bool = Field(..., description="Whether the operation succeeded.")
    blog_id: str | None = Field(
        default=None,
        description="ID of the saved blog post, if successful.",
    )
