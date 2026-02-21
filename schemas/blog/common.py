"""Shared Pydantic models reused across blog schemas."""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class BlogAuthorPersonalInfo(BaseModel):
    """Nested personal info of a blog author."""

    model_config = ConfigDict(extra="allow")

    fullname: Optional[str] = Field(default=None, description="Author's full name.")
    username: Optional[str] = Field(default=None, description="Author's username.")
    profile_img: Optional[str] = Field(default=None, description="Author's profile image URL.")


class BlogAuthor(BaseModel):
    """Author subdocument populated from the User model."""

    model_config = ConfigDict(extra="allow")

    personal_info: Optional[BlogAuthorPersonalInfo] = Field(
        default=None, description="Author's personal information.",
    )
