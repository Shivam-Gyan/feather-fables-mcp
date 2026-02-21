"""Pydantic schemas for user profile operations."""

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from urllib.parse import urlparse


SOCIAL_PLATFORMS = ["youtube", "instagram", "facebook", "twitter", "github", "website"]


class SocialLinks(BaseModel):
    """Social media links for a user profile."""

    model_config = ConfigDict(extra="forbid")

    youtube: str = Field(default="", description="YouTube channel URL.")
    instagram: str = Field(default="", description="Instagram profile URL.")
    facebook: str = Field(default="", description="Facebook profile URL.")
    twitter: str = Field(default="", description="Twitter/X profile URL.")
    github: str = Field(default="", description="GitHub profile URL.")
    website: str = Field(default="", description="Personal website URL.")

    @model_validator(mode="after")
    def validate_social_links(self) -> "SocialLinks":
        """Validate that each social link matches its platform hostname."""
        for platform in SOCIAL_PLATFORMS:
            url = getattr(self, platform)
            if not url:
                continue
            try:
                hostname = urlparse(url).hostname or ""
            except Exception:
                raise ValueError(f"Invalid URL for {platform}. Must include http(s)://")

            if platform != "website" and f"{platform}.com" not in hostname:
                raise ValueError(f"{platform} link is invalid. Expected a {platform}.com URL.")

        return self


class UpdateProfileInput(BaseModel):
    """Input schema for updating a user profile."""

    model_config = ConfigDict(strict=True, extra="forbid")

    username: str = Field(
        ...,
        description="Username (min 3 characters).",
        min_length=3,
    )
    bio: str = Field(
        default="",
        description="User bio (max 200 characters).",
        max_length=200,
    )
    social_links: SocialLinks = Field(
        default_factory=SocialLinks,
        description="Social media links.",
    )

    @field_validator("username")
    @classmethod
    def normalize_username(cls, v: str) -> str:
        """Strip whitespace and lowercase the username."""
        return v.strip().lower()


class UpdateProfileOutput(BaseModel):
    """Output schema for the update-profile operation."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(..., description="Whether the update succeeded.")
    message: str = Field(..., description="Human-readable result message.")
    username: str | None = Field(default=None, description="The updated username.")
